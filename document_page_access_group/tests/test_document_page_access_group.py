# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import Command
from odoo.exceptions import UserError
from odoo.tests.common import users

from odoo.addons.document_page_access_group import uninstall_hook

from .common import TestDocumentPageAccessGroupBase


class TestDocumentPageAccessGroup(TestDocumentPageAccessGroupBase):
    def test_page_access_constrains(self):
        with self.assertRaises(UserError):
            self.knowledge_page.write({"user_ids": [Command.set([self.user.id])]})

    @users("test-user")
    def test_page_access_01(self):
        pages = self.env["document.page"].search([])
        self.assertIn(self.public_page, pages)
        self.assertNotIn(self.knowledge_page, pages)
        self.assertIn(self.user_page, pages)

    @users("test-manager-user")
    def test_page_access_02(self):
        pages = self.env["document.page"].search([])
        self.assertIn(self.public_page, pages)
        self.assertIn(self.knowledge_page, pages)
        self.assertNotIn(self.user_page, pages)

    def test_uninstall_hook(self):
        accesses = self.env.ref("document_page.document_page_user") + self.env.ref(
            "document_page.document_page_editor"
        )
        self.assertFalse(any(accesses.mapped("active")))
        uninstall_hook(self.env)
        self.assertTrue(all(accesses.mapped("active")))
