# Copyright 2026 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import Command

from odoo.addons.base.tests.common import BaseCommon


class TestDesguaceparisCustom(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product_a = cls.env["product.product"].create({"name": "Test product A"})
        cls.product_tmpl_a = cls.product_a.product_tmpl_id
        cls.product_b = cls.env["product.product"].create({"name": "Test product B"})
        cls.product_tmpl_b = cls.product_b.product_tmpl_id
        cls.default_page = cls.env["document.page"].create({"name": "Test page"})

    def test_page_count(self):
        self.assertEqual(self.product_a.document_page_count, 0)
        self.assertEqual(self.product_tmpl_a.document_page_count, 0)
        self.assertEqual(self.product_b.document_page_count, 0)
        self.assertEqual(self.product_tmpl_b.document_page_count, 0)
        self.default_page.product_tmpl_ids = [Command.set(self.product_tmpl_a.ids)]
        self.assertEqual(self.product_a.document_page_count, 1)
        self.assertEqual(self.product_tmpl_a.document_page_count, 1)
        self.assertEqual(self.product_b.document_page_count, 0)
        self.assertEqual(self.product_tmpl_b.document_page_count, 0)
        self.assertIn(self.default_page, self.product_tmpl_a.document_page_ids)
        self.assertNotIn(self.default_page, self.product_tmpl_b.document_page_ids)
        action = self.product_a.action_document_page_products()
        self.assertEqual(
            action["domain"],
            [
                ("type", "=", "content"),
                ("product_tmpl_ids", "in", self.product_tmpl_a.ids),
            ],
        )
        self.assertEqual(
            action["context"],
            {
                "default_type": "content",
                "default_product_tmpl_ids": self.product_tmpl_a.ids,
            },
        )
        action = self.default_page.action_product_templates()
        self.assertEqual(action["domain"], [("id", "in", self.product_tmpl_a.ids)])
        self.assertEqual(action["context"], {})
