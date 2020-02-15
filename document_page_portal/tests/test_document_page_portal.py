# Copyright 2020 - TODAY, Marcel Savegnago - Escodoo
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl

import odoo.tests


@odoo.tests.tagged('post_install', '-at_install')
class TestUi(odoo.tests.HttpCase):
    def test_01_document_page_portal_tour(self):
        # Create a public document
        self.env['document.page'].create({
            'name': 'Test Public Page 1',
            'content': 'Test content',
            'is_public': True,
        })

        self.phantom_js(
            "/",
            "odoo.__DEBUG__.services['web_tour.tour']"
            ".run('document_page_portal_tour')",
            "odoo.__DEBUG__.services['web_tour.tour']"
            ".tours.document_page_portal_tour.ready",
            login="portal"
        )

        self.phantom_js(
            "/",
            "odoo.__DEBUG__.services['web_tour.tour']"
            ".run('document_page_portal_search_tour')",
            "odoo.__DEBUG__.services['web_tour.tour']"
            ".tours.document_page_portal_search_tour.ready",
            login="portal"
        )
