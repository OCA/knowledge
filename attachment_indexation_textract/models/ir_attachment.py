# Copyright 2023 len-foss/Financial Way
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging
import mimetypes
import tempfile

import textract

from odoo import models

_logger = logging.getLogger(__name__)


class IrAttachment(models.Model):
    _inherit = "ir.attachment"

    def _index(self, bin_data, mimetype, checksum=None):
        """Index documents with textract if available"""
        if mimetype != "application/pdf":  # mupdf is better
            buf = self.with_context(mimetype=mimetype)._index_textract(bin_data)
        return buf or super()._index(bin_data, mimetype, checksum=checksum)

    def _index_textract(self, bin_data):
        """Index documents with textract if available"""
        buf = ""
        try:
            mimetype = self.env.context.get("mimetype")
            extension = mimetypes.guess_extension(mimetype)
            with tempfile.NamedTemporaryFile(suffix=extension or "") as tmp_file:
                tmp_file.write(bin_data)
                file_path = tmp_file.name
                buf = textract.process(file_path)
        except Exception:
            _logger.info(Exception, exc_info=True)
        return buf
