# Copyright 2018 Onestein
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import base64

from odoo.tests.common import TransactionCase


class TestAttachmentPreview(TransactionCase):
    def test_get_extension(self):
        attachment = self.env["ir.attachment"].create(
            {"datas": base64.b64encode(b"from this, to that."), "name": "doc.txt"}
        )
        attachment2 = self.env["ir.attachment"].create(
            {"datas": base64.b64encode(b"Png"), "name": "image.png"}
        )
        res = self.env["ir.attachment"].get_attachment_extension(attachment.id)
        self.assertEqual(res, "txt")

        res = self.env["ir.attachment"].get_attachment_extension(
            [attachment.id, attachment2.id]
        )
        self.assertEqual(res[attachment.id], "txt")
        self.assertEqual(res[attachment2.id], "png")

        res2 = self.env["ir.attachment"].get_binary_extension(
            "ir.attachment", attachment.id, "datas"
        )
        self.assertTrue(res2)

        module = (
            self.env["ir.module.module"].search([]).filtered(lambda m: m.icon_image)[0]
        )
        res3 = self.env["ir.attachment"].get_binary_extension(
            "ir.module.module", module.id, "icon_image"
        )
        self.assertTrue(res3)

        module = (
            self.env["ir.ui.menu"].search([]).filtered(lambda m: not m.web_icon_data)[0]
        )
        res4 = self.env["ir.attachment"].get_binary_extension(
            "ir.ui.menu", module.id, "web_icon_data"
        )
        self.assertFalse(res4)
