# Copyright 2026 Ledoweb
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
"""
LibreOffice-based conversion endpoint for Office document preview.

Converts DOCX, XLSX, PPTX (and legacy DOC/XLS/PPT) to PDF for in-browser
viewing via the ViewerJS widget. LibreOffice headless must be installed;
if it is absent the endpoint returns HTTP 503.
"""

import base64
import os
import subprocess
import tempfile

from odoo import http
from odoo.http import request

# Extensions handled by LibreOffice conversion
OFFICE_EXTENSIONS = frozenset(
    {"docx", "xlsx", "pptx", "doc", "xls", "ppt", "odt", "ods", "odp", "odg"}
)


class AttachmentPreviewOfficeController(http.Controller):
    @http.route(
        "/attachment_preview/office_to_pdf",
        type="http",
        auth="user",
        methods=["GET"],
    )
    def office_to_pdf(self, model, field, id, filename="file", **kwargs):
        """Convert a binary field's Office document to PDF for preview.

        Query params:
            model   – Odoo model name (e.g. 'dms.file')
            field   – binary field name (e.g. 'content')
            id      – record id (integer)
            filename – original filename (used to derive extension)
        """
        try:
            record_id = int(id)
        except (TypeError, ValueError):
            return request.make_response("Bad request", status=400)

        record = request.env[model].browse(record_id)
        record.check_access("read")

        raw = getattr(record, field, None)
        if not raw:
            return request.make_response("No content", status=404)

        content = base64.b64decode(raw)
        ext = os.path.splitext(filename)[-1].lstrip(".").lower() or "bin"

        if ext not in OFFICE_EXTENSIONS:
            return request.make_response(
                "Extension not supported for conversion", status=415
            )

        pdf_bytes = self._libreoffice_to_pdf(content, ext)
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

    @staticmethod
    def _libreoffice_to_pdf(content, ext):
        """Run LibreOffice headless conversion. Returns PDF bytes or None."""
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                src = os.path.join(tmpdir, f"source.{ext}")
                with open(src, "wb") as fh:
                    fh.write(content)
                result = subprocess.run(
                    [
                        "libreoffice",
                        "--headless",
                        "--convert-to",
                        "pdf",
                        "--outdir",
                        tmpdir,
                        src,
                    ],
                    timeout=30,
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
