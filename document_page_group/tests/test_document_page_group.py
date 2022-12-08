# Copyright 2020 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestDocumentPageGroup(TransactionCase):
    def setUp(self):
        super().setUp()
        knowledge_group = self.browse_ref("document_knowledge.group_document_user").id
        self.user_id = self.env["res.users"].create(
            {
                "name": "user",
                "login": "login",
                "email": "email",
                "groups_id": [(4, knowledge_group)],
            }
        )
        self.group = self.browse_ref("document_page.group_document_manager")

        self.categ_1 = self.env["document.page"].create(
            {"name": "Categ 1", "type": "category"}
        )
        self.categ_2 = self.env["document.page"].create(
            {"name": "Categ 2", "type": "category", "parent_id": self.categ_1.id}
        )
        self.page = self.env["document.page"].create(
            {"name": "Page 1", "type": "content", "parent_id": self.categ_1.id}
        )

    def test_document_page_group(self):
        pages = (
            self.env["document.page"]
            .with_user(user=self.user_id.id)
            .search([("type", "=", "content")])
        )
        self.assertIn(self.page.id, pages.ids)

        self.categ_1.write({"direct_group_ids": [(4, self.group.id)]})
        self.assertIn(self.group.id, self.categ_2.group_ids.ids)

        pages = (
            self.env["document.page"]
            .with_user(user=self.user_id.id)
            .search([("type", "=", "content")])
        )
        self.assertNotIn(self.page.id, pages.ids)
