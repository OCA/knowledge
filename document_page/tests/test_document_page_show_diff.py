# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.exceptions import UserError

from odoo.addons.base.tests.common import BaseCommon


class TestDocumentPageShowDiff(BaseCommon):
    """document_page_show_diff test class."""

    _test_user_groups = ("document_page.group_document_manager",)

    def test_show_demo_page1_diff(self):
        """Show test page history difference."""
        page = self.env["document.page"].create(
            {
                "name": "Test Page",
                "content": "<div>Initial content</div>",
            }
        )

        show_diff_object = self.env["wizard.document.page.history.show_diff"]

        history_document = self.env["document.page.history"]
        history_pages = history_document.search([("page_id", "=", page.id)])

        self.assertTrue(
            show_diff_object.with_context(
                active_ids=[i.id for i in history_pages]
            )._get_diff()
        )

        page.write({"content": "<div>Text content updated</div>"})
        page.write({"content": "<div>Text updated</div>"})

        history_pages = history_document.search([("page_id", "=", page.id)])

        with self.assertRaises(UserError):
            show_diff_object.with_context(
                active_ids=[i.id for i in history_pages]
            )._get_diff()
