# Copyright 2020 - TODAY, Marcel Savegnago - Escodoo
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

import odoo.tests


@odoo.tests.tagged("post_install", "-at_install")
class TestPortalDocumentPage(odoo.tests.HttpCase):
    def test_01_document_page_portal_tour(self):
        # Create a public document
        self.env["document.page"].create(
            {
                "name": "Test Public Page 1",
                "content": "Test content",
                "is_public": True,
            }
        )
        self.start_tour("/", "document_page_portal_tour", login="portal")

    def test_02_document_page_portal_tour(self):
        self.start_tour("/", "document_page_portal_search_tour", login="portal")
