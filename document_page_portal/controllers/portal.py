from odoo.tests.common import HttpCase


class TestPortalController(HttpCase):
    def setUp(self):
        super(TestPortalController, self).setUp()
        self.document_page_model = self.env["document.page"]
        self.portal_controller = self.env["ir.http"].get(
            "portal.my.knowledge.document.pages"
        )

    def test_prepare_portal_layout_values(self):
        self.document_page_model.create({"name": "Test Page 1", "type": "content"})
        response = self.portal_controller()._prepare_portal_layout_values()
        self.assertIn("document_page_count", response)
        self.assertEqual(response["document_page_count"], 1)

    def test_get_archive_groups(self):
        self.document_page_model.create({"name": "Test Page 1", "type": "content"})
        domain = [("type", "=", "content")]
        groups = self.portal_controller()._get_archive_groups("document.page", domain)
        self.assertTrue(groups)
        self.assertEqual(groups[0]["name"], "Test Page 1")

    def test_portal_my_knowledge_document_pages(self):
        self.document_page_model.create({"name": "Test Page 1", "type": "content"})
        response = self.url_open("/my/knowledge/documents/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Test Page 1", response.data)

    def test_document_pages_followup(self):
        document_page = self.document_page_model.create(
            {"name": "Test Page 1", "type": "content"}
        )
        response = self.url_open(f"/knowledge/document/{document_page.id}")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Test Page 1", response.data)
