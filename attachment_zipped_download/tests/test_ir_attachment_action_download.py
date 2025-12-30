# Copyright 2023 Foodles (https://www.foodles.com/)
# @author Pierre Verkest <pierreverkest84@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import base64

from odoo import fields, models
from odoo.orm.model_classes import add_to_registry

from odoo.addons.base.tests.common import BaseCommon


class TestAttachmentDownload(models.TransientModel):
    _name = "test.attachment.download"
    _inherit = "ir.attachment.action_download"
    _description = "Test Attachment Download"

    name = fields.Char()


class TestIrAttachmentActionDownload(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        add_to_registry(cls.registry, TestAttachmentDownload)
        model_names = [TestAttachmentDownload._name]

        cls.registry._setup_models__(cls.env.cr, model_names)
        cls.registry.init_models(cls.env.cr, model_names, {"models_to_check": True})

        cls.addClassCleanup(cls.registry.__delitem__, TestAttachmentDownload._name)

        cls.test_model = cls.env[TestAttachmentDownload._name]

        cls.partner_1 = cls.test_model.create({"name": "Test partner 1"})
        cls.partner_2 = cls.test_model.create({"name": "Test partner 2"})
        cls.partner_3 = cls.test_model.create({"name": "Test partner 3"})

        cls.partner_1_f1 = cls._create_attachment(cls.partner_1, "partner_1-f1.txt")
        cls.partner_1_f2 = cls._create_attachment(cls.partner_1, "partner_1-f2.txt")
        cls.partner_2_f1 = cls._create_attachment(cls.partner_2, "partner_2-f1.txt")

    @classmethod
    def _create_attachment(cls, record, filename):
        return cls.env["ir.attachment"].create(
            {
                "name": filename,
                "res_model": record._name,
                "res_id": record.id,
                "type": "binary",
                "datas": base64.b64encode(b"Content"),
            }
        )

    def test_action_download_attachments_no_attachment(self):
        action = self.partner_3.action_download_attachments()
        self.assertEqual(action["type"], "ir.actions.client")
        self.assertEqual(action["tag"], "display_notification")

    def test_action_download_attachments_one_attachment(self):
        action = (self.partner_2 | self.partner_3).action_download_attachments()
        self.assertEqual(action["type"], "ir.actions.act_url")
        self.assertEqual(action["target"], "self")
        self.assertEqual(
            action["url"], f"/web/content/{self.partner_2_f1.id}?download=1"
        )

    def test_action_download_attachments_two_attachment_one_record(self):
        action = (self.partner_1).action_download_attachments()
        self.assertEqual(action["type"], "ir.actions.act_url")
        self.assertEqual(action["target"], "self")
        self.assertTrue(action["url"].startswith("/web/attachment/download_zip?ids="))
        ids = sorted(map(int, action["url"].split("=")[1].split(",")))
        self.assertEqual(ids, (self.partner_1_f1 | self.partner_1_f2).ids)

    def test_action_download_attachments_three_attachment_n_records(self):
        action = (
            self.partner_1 | self.partner_2 | self.partner_3
        ).action_download_attachments()
        self.assertEqual(action["type"], "ir.actions.act_url")
        self.assertEqual(action["target"], "self")
        self.assertTrue(action["url"].startswith("/web/attachment/download_zip?ids="))
        ids = sorted(map(int, action["url"].split("=")[1].split(",")))
        self.assertEqual(
            ids, (self.partner_1_f1 + self.partner_1_f2 + self.partner_2_f1).ids
        )
