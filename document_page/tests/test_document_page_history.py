from odoo.tests import common


class TestDocumentPageHistory(common.TransactionCase):
    """document_page_history test class."""

    def test_page_history_demo_page1(self):
        """Test page history demo page1."""
        page = self.env.ref("document_page.demo_page1")
        page.content = "Test content updated"
        history_document = self.env["document.page.history"]
        history_pages = history_document.search([("page_id", "=", page.id)])
        active_ids = [i.id for i in history_pages]

        result = history_document._get_diff(active_ids[0], active_ids[0])
        self.assertEqual(result, "There are no changes in revisions.")

        result = history_document._get_diff(active_ids[0], active_ids[1])
        self.assertNotEqual(result, "There are no changes in revisions.")
