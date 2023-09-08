# Copyright 2023 len-foss/Financial Way
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import io
import logging

from odoo import models

_logger = logging.getLogger(__name__)

try:
    import fitz
except ImportError:
    fitz = None
    _logger.warning(
        "Attachment indexation of PDF documents is unavailable"
        "because PyMuPDF cannot be loaded."
    )


class IrAttachment(models.Model):
    _inherit = "ir.attachment"

    def _index_pdf(self, bin_data):
        """Index PDF documents with MuPDF if available"""
        if fitz is None:
            return super()._index_pdf(bin_data)
        buf = ""
        try:
            f = io.BytesIO(bin_data)
            doc = fitz.open(stream=f, filetype="pdf")
            for page in doc:
                buf += page.get_text()
        except Exception:  # pylint: disable=except-pass
            pass
        return buf
