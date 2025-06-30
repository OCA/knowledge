# Copyright 2024 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.tests.common import users

from odoo.addons.document_page_access_group.tests.common import (
    TestDocumentPageAccessGroupBase,
)


class TestDocumentPageAccessGroupUserRole(TestDocumentPageAccessGroupBase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_role = cls.env["res.users.role"].create(
            {
                "name": "Test role",
                "implied_ids": [(6, 0, [cls.group.id])],
                "users": [(6, 0, [cls.manager_user.id])],
            }
        )
        cls.role_page = cls.env["document.page"].create(
            {
                "name": "Role Page (test role)",
                "type": "content",
                "role_ids": [(6, 0, [cls.user_role.id])],
            }
        )

    def test_document_page_role_misc(self):
        self.assertFalse(self.role_page.groups_id)
        self.assertTrue(self.role_page.user_ids)

    @users("test-user")
    def test_document_page_role_access_01(self):
        pages = self.env["document.page"].search([])
        self.assertIn(self.public_page, pages)
        self.assertNotIn(self.knowledge_page, pages)
        self.assertIn(self.user_page, pages)
        self.assertNotIn(self.role_page, pages)

    @users("test-manager-user")
    def test_document_page_role_access_02(self):
        pages = self.env["document.page"].search([])
        self.assertIn(self.public_page, pages)
        self.assertIn(self.knowledge_page, pages)
        self.assertNotIn(self.user_page, pages)
        self.assertIn(self.role_page, pages)
