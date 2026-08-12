# Copyright 2026 Jarsa
# Copyright 2026 Ledoweb
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
"""LibreOffice-based conversion endpoint for office-document preview.

Converts office documents (ODF *and* OOXML: ODT/ODS/ODP, DOCX/XLSX/PPTX,
macro-enabled DOCM/XLSM/PPTM, legacy DOC/XLS/PPT, ODG) to PDF so they can be
rendered by Odoo's native PDF.js viewer.
LibreOffice headless must be installed; if it is absent the endpoint returns
HTTP 503.
"""

import base64
import hashlib
import io
import logging
import os
import re
import subprocess
import tempfile
import zipfile

from odoo import http, tools
from odoo.http import request

_logger = logging.getLogger(__name__)

# Office formats LibreOffice can convert to PDF (ODF + OOXML + legacy binary).
OFFICE_EXTENSIONS = frozenset(
    {
        "docx",
        "docm",
        "xlsx",
        "xlsm",
        "pptx",
        "pptm",
        "doc",
        "xls",
        "ppt",
        "odt",
        "ods",
        "odp",
        "odg",
    }
)

# Spreadsheets are exported with the SinglePageSheets option (one full-size
# page per sheet) so columns are not cut by Calc's print pagination. The
# option is seeded into the isolated LibreOffice profile registry instead of
# being passed as CLI filter options: the JSON filter-options syntax is only
# parsed by LibreOffice >= 7.4, while the registry works from 7.2.
SPREADSHEET_EXTENSIONS = frozenset({"xlsx", "xlsm", "xls", "ods"})
SINGLE_PAGE_SHEETS_XCU = """<?xml version="1.0" encoding="UTF-8"?>
<oor:items xmlns:oor="http://openoffice.org/2001/registry"
 xmlns:xs="http://www.w3.org/2001/XMLSchema"
 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
 <item oor:path="/org.openoffice.Office.Common/Filter/PDF/Export">
  <prop oor:name="SinglePageSheets" oor:op="fuse"><value>true</value></prop>
 </item>
</oor:items>
"""
# With SinglePageSheets, LibreOffice starts the export at the sheet's saved
# scroll position (sheetView topLeftCell) instead of at the top of the used
# range, so a workbook saved while scrolled down loses every row above the
# visible area. The saved scroll is presentation-only, so it is stripped from
# OOXML spreadsheets before conversion. Legacy binary .xls (and .ods) cannot
# be patched this way and keep the upstream behavior.
OOXML_SPREADSHEET_EXTENSIONS = frozenset({"xlsx", "xlsm"})
TOP_LEFT_CELL_RE = re.compile(rb'\stopLeftCell="[^"]*"')

# Bump to invalidate PDFs cached before a conversion-behavior change.
CACHE_KEY_VERSION = "3"

# Reject documents larger than this before spawning a (slow) conversion.
MAX_CONTENT_BYTES = 50 * 1024 * 1024  # 50 MB
# Per-conversion wall-clock budget (seconds).
CONVERT_TIMEOUT = 60


class AttachmentPreviewOfficeController(http.Controller):
    @http.route(
        "/attachment_preview_office/to_pdf",
        type="http",
        auth="user",
        methods=["GET"],
    )
    def office_to_pdf(  # pylint: disable=redefined-builtin
        self, model, field, id, filename="file", **kwargs
    ):
        """Convert a binary field's office document to PDF for preview.

        Query params:
            model    – Odoo model name (e.g. 'ir.attachment')
            field    – binary field name (e.g. 'datas')
            id       – record id (integer)
            filename – original filename (used to derive the extension)
        """
        try:
            record_id = int(id)
        except (TypeError, ValueError):
            return request.make_response("Bad request", status=400)

        # Extension allow-list (on the claimed filename) before touching the DB.
        ext = os.path.splitext(filename)[-1].lstrip(".").lower()
        if ext not in OFFICE_EXTENSIONS:
            return request.make_response(
                "Extension not supported for conversion", status=415
            )

        record = request.env[model].browse(record_id).exists()
        if not record:
            return request.make_response("Not found", status=404)
        # Record-level ACL: raises AccessError (-> 403) if the user can't read.
        record.check_access_rights("read")
        record.check_access_rule("read")

        # The field must exist on the model AND be a binary field — never read
        # an arbitrary attribute supplied in the query string.
        model_field = record._fields.get(field)
        if model_field is None or model_field.type != "binary":
            return request.make_response("Invalid field", status=400)

        raw = record[field]
        if not raw:
            return request.make_response("No content", status=404)

        content = base64.b64decode(raw)
        if len(content) > MAX_CONTENT_BYTES:
            return request.make_response("Document too large to preview", status=413)

        pdf_bytes = self._get_pdf_cached(content, ext)
        if pdf_bytes is None:
            return request.make_response(
                "LibreOffice not available — cannot convert document", status=503
            )

        return request.make_response(
            pdf_bytes,
            headers=[
                ("Content-Type", "application/pdf"),
                (
                    "Content-Disposition",
                    f'inline; filename="{os.path.splitext(filename)[0]}.pdf"',
                ),
                ("Cache-Control", "private, max-age=3600"),
            ],
        )

    # -- conversion + cache ----------------------------------------------------

    def _get_pdf_cached(self, content, ext):
        """Return converted PDF bytes, using a checksum-keyed disk cache.

        The cache lives under the Odoo filestore so it is shared across workers
        on the same host; identical documents are converted only once. All cache
        I/O is best-effort: a miss or any filesystem error falls back silently to
        a fresh conversion.
        """
        # The extension is part of the key: the export options depend on it.
        key = f"{hashlib.sha256(content).hexdigest()}-{ext}-{CACHE_KEY_VERSION}"
        cache_path = self._cache_path(key)
        if cache_path and os.path.exists(cache_path):
            try:
                with open(cache_path, "rb") as fh:
                    return fh.read()
            except OSError:
                _logger.warning(
                    "attachment_preview_office: cache read failed", exc_info=True
                )

        pdf_bytes = self._libreoffice_to_pdf(content, ext)
        if pdf_bytes and cache_path:
            try:
                # Atomic publish so a concurrent reader never sees a partial file.
                tmp = f"{cache_path}.{os.getpid()}.tmp"
                with open(tmp, "wb") as fh:
                    fh.write(pdf_bytes)
                os.replace(tmp, cache_path)
            except OSError:
                _logger.warning(
                    "attachment_preview_office: cache write failed", exc_info=True
                )
        return pdf_bytes

    @staticmethod
    def _cache_path(key):
        """Return the cache file path for ``key`` under the filestore, or None."""
        try:
            base = os.path.join(
                tools.config.filestore(request.env.cr.dbname),
                "attachment_preview_office_cache",
            )
            os.makedirs(base, exist_ok=True)
            return os.path.join(base, f"{key}.pdf")
        except Exception:  # pragma: no cover - never let caching break preview
            return None

    @staticmethod
    def _strip_saved_scroll(content):
        """Remove the saved scroll position from an OOXML spreadsheet.

        Rewrites the zip dropping the ``topLeftCell`` attribute from every
        ``xl/worksheets/*.xml`` so the SinglePageSheets export starts at the
        top of each sheet. On any error the original content is returned and
        LibreOffice gets to try the file as-is.
        """
        try:
            out = io.BytesIO()
            with (
                zipfile.ZipFile(io.BytesIO(content)) as zin,
                zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zout,
            ):
                for item in zin.infolist():
                    data = zin.read(item.filename)
                    if item.filename.startswith("xl/worksheets/"):
                        data = TOP_LEFT_CELL_RE.sub(b"", data)
                    zout.writestr(item, data)
            return out.getvalue()
        except Exception:  # pylint: disable=broad-except
            return content

    @staticmethod
    def _libreoffice_to_pdf(content, ext):
        """Run LibreOffice headless conversion. Returns PDF bytes or None.

        Each invocation uses an isolated ``UserInstallation`` profile so that
        concurrent conversions do not collide on the shared LibreOffice profile
        lock — the classic "another instance is already running" failure that
        otherwise makes this endpoint flaky under any real load.
        """
        if ext in OOXML_SPREADSHEET_EXTENSIONS:
            content = AttachmentPreviewOfficeController._strip_saved_scroll(content)
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                src = os.path.join(tmpdir, f"source.{ext}")
                with open(src, "wb") as fh:
                    fh.write(content)
                profile = os.path.join(tmpdir, "louser")
                if ext in SPREADSHEET_EXTENSIONS:
                    user_dir = os.path.join(profile, "user")
                    os.makedirs(user_dir, exist_ok=True)
                    xcu = os.path.join(user_dir, "registrymodifications.xcu")
                    with open(xcu, "w", encoding="utf-8") as fh:
                        fh.write(SINGLE_PAGE_SHEETS_XCU)
                result = subprocess.run(
                    [
                        "libreoffice",
                        f"-env:UserInstallation=file://{profile}",
                        "--headless",
                        "--convert-to",
                        "pdf",
                        "--outdir",
                        tmpdir,
                        src,
                    ],
                    timeout=CONVERT_TIMEOUT,
                    capture_output=True,
                )
                if result.returncode != 0:
                    _logger.warning(
                        "LibreOffice conversion failed (exit %s): %s",
                        result.returncode,
                        result.stderr.decode("utf-8", errors="replace")[-500:],
                    )
                    return None
                pdf_path = os.path.join(tmpdir, "source.pdf")
                if not os.path.exists(pdf_path):
                    return None
                with open(pdf_path, "rb") as fh:
                    return fh.read()
        except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
            return None
