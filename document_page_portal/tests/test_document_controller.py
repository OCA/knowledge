from unittest.mock import patch

from odoo.tests import common
from odoo.tests.common import tagged

from odoo.addons.document_page_portal.controllers.portal import CustomerPortal


@tagged("post_install", "-at_install")
class TestCustomerPortal(common.HttpCase):
    def setUp(self):
        super(TestCustomerPortal, self).setUp()
        self.customer_portal = CustomerPortal()
        self.document_page = self.env["document.page"].create(
            {
                "name": "Test Document Page",
                "content": "Test Content",
                "type": "content",
            }
        )

    def _mock_request(self):
        mock_request = type("MockRequest", (), {})()
        mock_request.env = self.env
        mock_request.session = {}
        return mock_request

    @patch("odoo.http.request")
    def test_get_archive_groups(self, mock_request):
        mock_request.env = self.env
        groups = self.customer_portal._get_archive_groups("document.page")
        self.assertTrue(groups)

    @patch("odoo.http.request")
    def test_document_page_get_page_view_values(self, mock_request):
        mock_request.env = self.env
        mock_request.session = {}
        values = self.customer_portal._document_page_get_page_view_values(
            self.document_page, "test_token"
        )
        self.assertEqual(values["page_name"], "document_page")
        self.assertEqual(values["document_page"], self.document_page)

    def test_portal_my_knowledge_document_pages(self):
        self.authenticate("admin", "admin")
        response = self.url_open("/my/knowledge/documents/")
        self.assertEqual(response.status_code, 200)

        # Test with search parameters
        response = self.url_open(
            "/my/knowledge/documents/?search=Test&search_in=content"
        )
        self.assertEqual(response.status_code, 200)

    def test_document_pages_followup(self):
        self.authenticate("admin", "admin")
        response = self.url_open(f"/knowledge/document/{self.document_page.id}")
        self.assertEqual(response.status_code, 200)

        # Test with invalid document_page_id
        response = self.url_open("/knowledge/document/9999")
        self.assertEqual(response.status_code, 303)  # Should redirect to /my
