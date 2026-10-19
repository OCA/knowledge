# Copyright 2026 Escodoo
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import HttpCase, tagged


@tagged("post_install", "-at_install")
@tagged("post_install", "-at_install")
class TestMarkdownPowerbox(HttpCase):
    def test_markdown_powerbox_tour(self):
        category = self.env["document.page"].create(
            {"name": "Powerbox category", "type": "category"}
        )
        page = self.env["document.page"].create(
            {
                "name": "Powerbox page",
                "parent_id": category.id,
                "content": "<p>Start here</p>",
                "draft_name": "1.0",
                "draft_summary": "initial",
            }
        )
        self.start_tour(
            "/web#id=%s&model=document.page&view_type=form" % page.id,
            "document_page_markdown_powerbox_tour",
            login="admin",
        )
