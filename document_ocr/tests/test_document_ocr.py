# -*- coding: utf-8 -*-
# © 2016 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from PIL import Image, ImageDraw, ImageFont
from StringIO import StringIO
from openerp.tests.common import TransactionCase
from openerp.addons.document_ocr.models.ir_attachment import _MARKER_PHRASE


class TestDocumentOcr(TransactionCase):
    def test_document_ocr(self):
        self.env['ir.config_parameter'].set_param(
            'document_ocr.synchronous', 'True')
        test_image = Image.new('RGB', (200, 30))
        draw = ImageDraw.Draw(test_image)
        draw.text((3, 3), "Hello world", font=ImageFont.truetype(
            '/usr/share/fonts/truetype/inconsolata/Inconsolata.otf', 24))
        # test a plain image
        data = StringIO()
        test_image.save(data, 'png')
        result = self.env['ir.attachment']._index(
            data.getvalue(), 'test.png', None)
        self.assertEqual(result[1].strip(), 'Hello world')
        # should also work for pdfs
        data = StringIO()
        test_image.save(data, 'pdf', resolution=300)
        result = self.env['ir.attachment']._index(
            data.getvalue(), 'test.pdf', None)
        self.assertEqual(result[1].strip(), 'Hello world')
        # check cron
        self.env['ir.config_parameter'].set_param(
            'document_ocr.synchronous', 'False')
        attachment = self.env['ir.attachment'].create({
            'name': 'testattachment',
            'datas': data.getvalue().encode('base64'),
        })
        self.assertEqual(attachment.index_content, _MARKER_PHRASE)
        attachment._ocr_cron()
        self.assertEqual(attachment.index_content.strip(), 'Hello world')
        # and for an unreadable image, we expect an error
        self.env['ir.config_parameter'].set_param(
            'document_ocr.synchronous', 'True')
        data = StringIO()
        test_image = Image.new('1', (200, 30))
        test_image.save(data, 'Palm')
        result = self.env['ir.attachment']._index(
            data.getvalue(), 'test.palm', None)
        self.assertEqual(result[1], None)
