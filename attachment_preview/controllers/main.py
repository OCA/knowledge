# Copyright 2026 Ledoweb
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
"""LibreOffice-based conversion endpoint for office-document preview.

Converts office documents (ODF *and* OOXML: ODT/ODS/ODP, DOCX/XLSX/PPTX, legacy
DOC/XLS/PPT, ODG) to PDF so they can be rendered by Odoo's native PDF.js viewer.
LibreOffice headless must be installed; if it is absent the endpoint returns
HTTP 503.
"""

import base64
import hashlib
import logging
import os
import subprocess
import tempfile

from odoo import http, tools
from odoo.http import request

_logger = logging.getLogger(__name__)

# Office formats LibreOffice can convert to PDF (ODF + OOXML + legacy binary).
OFFICE_EXTENSIONS = frozenset(
    {"docx", "xlsx", "pptx", "doc", "xls", "ppt", "odt", "ods", "odp", "odg"}
)

# Reject documents larger than this before spawning a (slow) conversion.
MAX_CONTENT_BYTES = 50 * 1024 * 1024  # 50 MB
# Per-conversion wall-clock budget (seconds).
CONVERT_TIMEOUT = 60


class AttachmentPreviewOfficeController(http.Controller):
    @http.route(
        "/attachment_preview/office_to_pdf",
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
        record.check_access("read")

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

        The cache lives under the Odoo data_dir so it is shared across workers
        on the same host; identical documents are converted only once. All cache
        I/O is best-effort: a miss or any filesystem error falls back silently to
        a fresh conversion.
        """
        key = hashlib.sha256(content).hexdigest()
        cache_path = self._cache_path(key)
        if cache_path and os.path.exists(cache_path):
            try:
                with open(cache_path, "rb") as fh:
                    return fh.read()
            except OSError:
                _logger.warning("attachment_preview: cache read failed", exc_info=True)

        pdf_bytes = self._libreoffice_to_pdf(content, ext)
        if pdf_bytes and cache_path:
            try:
                # Atomic publish so a concurrent reader never sees a partial file.
                tmp = f"{cache_path}.{os.getpid()}.tmp"
                with open(tmp, "wb") as fh:
                    fh.write(pdf_bytes)
                os.replace(tmp, cache_path)
            except OSError:
                _logger.warning("attachment_preview: cache write failed", exc_info=True)
        return pdf_bytes

    @staticmethod
    def _cache_path(key):
        """Return the cache file path for ``key`` under the data_dir, or None."""
        try:
            base = os.path.join(
                tools.config.filestore(request.env.cr.dbname),
                "attachment_preview_cache",
            )
            os.makedirs(base, exist_ok=True)
            return os.path.join(base, f"{key}.pdf")
        except Exception:  # pragma: no cover - never let caching break preview
            return None

    @staticmethod
    def _libreoffice_to_pdf(content, ext):
        """Run LibreOffice headless conversion. Returns PDF bytes or None.

        Each invocation uses an isolated ``UserInstallation`` profile so that
        concurrent conversions do not collide on the shared LibreOffice profile
        lock — the classic "another instance is already running" failure that
        otherwise makes this endpoint flaky under any real load.
        """
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                src = os.path.join(tmpdir, f"source.{ext}")
                with open(src, "wb") as fh:
                    fh.write(content)
                profile = os.path.join(tmpdir, "louser")
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
                    return None
                pdf_path = os.path.join(tmpdir, "source.pdf")
                if not os.path.exists(pdf_path):
                    return None
                with open(pdf_path, "rb") as fh:
                    return fh.read()
        except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
            return None
