# © 2016 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import base64
import subprocess
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont

from odoo.tests.common import TransactionCase

from ..models.ir_attachment import _MARKER_PHRASE


def _get_some_system_font():
    """Get a font that is available on the system"""
    output = subprocess.check_output(["fc-list"])
    for line in output.splitlines():
        line = line.decode("utf-8")
        if "otf" in line.lower() and "roman" in line.lower():
            return line.split(":")[0]
    raise RuntimeError("No suitable font found!")


font_path = _get_some_system_font()
ir_config_parameter_key = "ocr.synchronous"
result_string = "Hello world"


def _get_image_data(frmt="png"):
    test_image = Image.new("RGB", (200, 30))
    draw = ImageDraw.Draw(test_image)
    draw.text((3, 3), result_string, font=ImageFont.truetype(font_path, 24))
    data = BytesIO()
    test_image.save(data, frmt)
    return data.getvalue()


class TestDocumentOcr(TransactionCase):
    def test_document_ocr_png(self):
        self.env["ir.config_parameter"].set_param(ir_config_parameter_key, "True")
        bin_data = _get_image_data("png")
        result = self.env["ir.attachment"]._index(bin_data, "image/png")
        self.assertEqual(result.strip(), result_string)

    def test_document_ocr_ppm(self):
        """It works on images that don't have a specific mimetype"""
        self.env["ir.config_parameter"].set_param(ir_config_parameter_key, "True")
        bin_data = _get_image_data("ppm")
        result = self.env["ir.attachment"]._index(bin_data, "application/octet-stream")
        self.assertEqual(result.strip(), result_string)

    def test_document_ocr_pdf(self):
        self.env["ir.config_parameter"].set_param(ir_config_parameter_key, "True")
        bin_data = _get_image_data("pdf")
        result = self.env["ir.attachment"]._index(bin_data, "application/pdf")
        self.assertEqual(result.strip(), result_string)

    def test_document_ocr_cron(self):
        self.env["ir.config_parameter"].set_param(ir_config_parameter_key, "False")
        bin_data = _get_image_data("png")
        vals = {"name": "testattachment", "datas": base64.b64encode(bin_data)}
        attachment = self.env["ir.attachment"].create(vals)
        self.assertEqual(attachment.index_content, _MARKER_PHRASE)
        attachment._ocr_cron()
        self.assertEqual(attachment.index_content.strip(), result_string)
