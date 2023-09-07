# © 2016 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import base64
import logging
import subprocess
from io import BytesIO

from PIL import Image

from odoo import api, models

_logger = logging.getLogger(__name__)
_MARKER_PHRASE = "[[waiting for OCR]]"


class IrAttachment(models.Model):
    _inherit = "ir.attachment"

    @api.model
    def _get_no_content_strings(self):
        return ["image", "application"]

    @api.model
    def _not_content(self, text):
        return not text or text in self._get_no_content_strings()

    @api.model
    def _index(self, bin_data, file_type, checksum=None):
        content = super()._index(bin_data, file_type, checksum)
        if bin_data and file_type and self._not_content(content):
            synchronous = self.env["ir.config_parameter"].get_param("ocr.synchronous")
            if synchronous == "True" or self.env.context.get("ocr_force"):
                content = self._index_ocr(bin_data, file_type)
            else:
                content = _MARKER_PHRASE
        return content

    @api.model
    def _index_ocr(self, bin_data, file_type, dpi=0):
        if not dpi:
            icp = self.env["ir.config_parameter"]
            dpi = int(icp.get_param("ocr.dpi", "500"))
        if "/" not in file_type:
            _logger.warning("Invalid mimetype %s", file_type)
            return None
        top_type, sub_type = file_type.split("/", 1)
        if sub_type == "pdf":
            # tesseract only supports image of at most 32K pixels
            # depending on the number of pages, we have to either split
            # into different batches or reduce the dpi;
            # The maximum width and height are 32767.
            image_data = self._index_ocr_get_data_pdf(bin_data, dpi)  # TODO
        else:
            image_data = BytesIO()
            try:
                i = Image.open(BytesIO(bin_data))
                i.save(image_data, "png", dpi=(dpi, dpi))
            except IOError:
                _logger.exception("Failed to OCR image")
                return None
        process = subprocess.Popen(
            ["tesseract", "stdin", "stdout"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout, stderr = process.communicate(image_data.getvalue())
        if process.returncode:
            _logger.error("Error during OCR: %s", stderr)
        return stdout.decode("utf-8")

    @api.model
    def _index_ocr_get_data_pdf(self, bin_data, dpi):
        process = subprocess.Popen(
            ["convert", "-density", str(dpi), "-", "-append", "png32:-"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout, stderr = process.communicate(bin_data)
        if stderr:
            _logger.error("Error converting to PDF: %s", stderr)
        return BytesIO(stdout)

    @api.model
    def _ocr_cron(self, limit=None):
        domain = [("index_content", "=", _MARKER_PHRASE)]
        recs = self.with_context(ocr_force=True).search(domain, limit=limit)
        recs.perform_ocr()

    def perform_ocr(self):
        for rec in self:
            if not rec.datas:
                index_content = ""  # the _MARKER_PHRASE should be removed
            else:
                bin_data = base64.b64decode(rec.datas)
                ctx = {"ocr_force": True}
                index_content = rec.with_context(**ctx)._index(bin_data, rec.mimetype)
            rec.write({"index_content": index_content})
