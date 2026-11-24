from odoo.addons.base.tests.common import BaseCommon


class TestDocumentPageHistory(BaseCommon):
    """document_page_history test class."""

    _test_user_groups = ("document_page.group_document_manager",)

    def test_page_history_demo_page1(self):
        """Test page history demo page1."""
        page = self.env["document.page"].create(
            {
                "name": "Test Page",
                "content": "<div>Initial content</div>",
            }
        )
        page.content = "<div>Test content updated</div>"
        history_document = self.env["document.page.history"]
        history_pages = history_document.search([("page_id", "=", page.id)])
        active_ids = [i.id for i in history_pages]
        result = history_document._get_diff(active_ids[0], active_ids[0])
        self.assertEqual(result, page.content)
