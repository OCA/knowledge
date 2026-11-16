from odoo.tests import common


class TestDocumentPageHistory(common.TransactionCase):
    """document_page_history test class."""

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

    def test_history_display_name(self):
        """History display_name must be a plain string, not a (id, name) tuple."""
        page = self.env["document.page"].create(
            {
                "name": "Test Page",
                "content": "<div>Initial content</div>",
            }
        )
        page.content = "<div>Test content updated</div>"
        history_pages = self.env["document.page.history"].search(
            [("page_id", "=", page.id)]
        )
        self.assertTrue(history_pages)
        for rec in history_pages:
            self.assertEqual(rec.display_name, f"{page.name} #{rec.id}")
