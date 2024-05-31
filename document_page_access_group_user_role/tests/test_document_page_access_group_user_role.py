# Copyright 2024 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.base.tests.common import BaseCommon


class TestDocumentPageAccessGroupUserRole(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.page = cls.env["document.page"].create(
            {"name": "Page 1", "type": "content"}
        )
        cls.group_a = cls.env["res.groups"].create({"name": "Test group A"})
        cls.group_b = cls.env["res.groups"].create({"name": "Test group B"})
        cls.user_role = cls.env["res.users.role"].create(
            {"name": "Test role", "implied_ids": [(6, 0, [cls.group_a.id])]}
        )

    def test_document_page_role(self):
        self.assertFalse(self.page.groups_id)
        self.page.role_ids = [(4, self.user_role.id)]
        self.assertIn(self.group_a, self.page.groups_id)
        self.assertNotIn(self.group_b, self.page.groups_id)
        self.user_role.implied_ids = [(4, self.group_b.id)]
        self.assertIn(self.group_a, self.page.groups_id)
        self.assertIn(self.group_b, self.page.groups_id)
        self.page.role_ids = [(6, 0, [])]
        self.assertNotIn(self.group_a, self.page.groups_id)
        self.assertNotIn(self.group_b, self.page.groups_id)
