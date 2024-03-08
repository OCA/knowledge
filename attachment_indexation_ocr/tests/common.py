# Copyright 2023 len-foss/Financial Way
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import subprocess
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont

from odoo.tests.common import TransactionCase

from ..models.ir_attachment import _MARKER_PHRASE


class TestOcrCase(TransactionCase):
    @classmethod
    def _get_some_system_font(cls):
        """Get a font that is available on the system"""
        output = subprocess.check_output(["fc-list"])
        for line in output.splitlines():
            line = line.decode("utf-8")
            if "otf" in line.lower() and "roman" in line.lower():
                return line.split(":")[0]
        raise RuntimeError("No suitable font found!")

    @classmethod
    def _get_image_data(cls, frmt):
        test_image = Image.new("RGB", (200, 30))
        draw = ImageDraw.Draw(test_image)
        font = ImageFont.truetype(cls.font_path, 24)
        draw.text((3, 3), cls.result_string, font=font)
        data = BytesIO()
        test_image.save(data, frmt)
        return data.getvalue()

    @classmethod
    def setUpClass(cls):
        super(TestOcrCase, cls).setUpClass()

        cls.font_path = cls._get_some_system_font()
        cls.ir_config_parameter_key = "ocr.synchronous"
        cls.result_string = "Hello world"
        cls.data_png = cls._get_image_data("png")
        cls.marker = _MARKER_PHRASE

        cls.attachment_ocr = cls.env["ir.attachment"].with_context(ocr_force=True)
