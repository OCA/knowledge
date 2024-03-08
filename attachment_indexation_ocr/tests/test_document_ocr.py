# © 2016 Therp BV <http://therp.nl>
# Copyright 2023 len-foss/Financial Way
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import base64

from .common import TestOcrCase


class TestOcr(TestOcrCase):
    def test_document_ocr_png(self):
        result = self.attachment_ocr._index(self.data_png, "image/png")
        self.assertEqual(result.strip(), self.result_string)

    def test_document_ocr_ppm(self):
        """It works on images that don't have a specific mimetype"""
        bin_data = self._get_image_data("ppm")
        result = self.attachment_ocr._index(bin_data, "application/octet-stream")
        self.assertEqual(result.strip(), self.result_string)

    def test_document_ocr_pdf(self):
        bin_data = self._get_image_data("pdf")
        result = self.attachment_ocr._index(bin_data, "application/pdf")
        self.assertEqual(result.strip(), self.result_string)

    def test_document_ocr_cron(self):
        vals = {"name": "testattachment", "datas": base64.b64encode(self.data_png)}
        attachment = self.env["ir.attachment"].create(vals)
        self.assertEqual(attachment.index_content, self.marker)
        attachment._ocr_cron()
        self.assertEqual(attachment.index_content.strip(), self.result_string)

    def test_document_ocr_lang(self):
        """We can pass an ocr_lang context key to help text detection"""
        bin_data = self._get_image_data("pdf")
        with_lang = self.attachment_ocr.with_context(ocr_lang="eng")
        result = with_lang._index(bin_data, "application/pdf")
        self.assertEqual(result.strip(), self.result_string)
