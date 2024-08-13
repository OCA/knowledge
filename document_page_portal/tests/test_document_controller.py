# Path: addons/document_page_portal/tests/test_document_controller.py

from odoo import fields as odoo_fields
from odoo.exceptions import AccessError, MissingError
from odoo.tests.common import HttpCase, tagged


@tagged("post_install", "-at_install")
class TestDocumentPagePortal(HttpCase):
    def setUp(self):
        super(TestDocumentPagePortal, self).setUp()
        self.portal_user = self.env.ref("base.public_user")
        self.document_page_model = self.env["document.page"]

    def test_prepare_portal_layout_values(self):
        """Test _prepare_portal_layout_values method."""
        # Manually call the method from the controller instance
        portal_controller = (
            self.env["ir.http"]
            .sudo()
            ._get_class(
                "odoo.addons.document_page_portal.controllers.portal.CustomerPortal"
            )()
        )
        values = portal_controller._prepare_portal_layout_values()
        document_page_count = self.document_page_model.search_count(
            [("type", "=", "content")]
        )
        self.assertEqual(values.get("document_page_count"), document_page_count)

    def test_get_archive_groups(self):
        """Test _get_archive_groups method."""
        # Manually call the method from the controller instance
        portal_controller = (
            self.env["ir.http"]
            .sudo()
            ._get_class(
                "odoo.addons.document_page_portal.controllers.portal.CustomerPortal"
            )()
        )

        domain = [("type", "=", "content")]
        groups = portal_controller._get_archive_groups("document.page", domain)
        self.assertTrue(isinstance(groups, list))
        self.assertGreaterEqual(
            len(groups), 0
        )  # Depending on the data, there could be 0 or more groups

    def test_portal_my_knowledge_document_pages(self):
        """Test portal_my_knowledge_document_pages route."""
        with self.env.cr.savepoint():
            self.env = self.env(user=self.portal_user)
            result = self.url_open("/my/knowledge/documents")
            self.assertEqual(result.status_code, 200)

            # Test with search query
            result = self.url_open("/my/knowledge/documents?search=test")
            self.assertEqual(result.status_code, 200)

            # Test with date filter
            date_begin = odoo_fields.Date.to_string(odoo_fields.Date.today())
            date_end = odoo_fields.Date.to_string(odoo_fields.Date.today())
            result = self.url_open(
                f"/my/knowledge/documents?date_begin={date_begin}&date_end={date_end}"
            )
            self.assertEqual(result.status_code, 200)

    def test_document_pages_followup(self):
        """Test document_pages_followup route."""
        with self.env.cr.savepoint():
            self.env = self.env(user=self.portal_user)
            # Create a document.page record to test with
            document_page = self.document_page_model.create(
                {"name": "Test Document", "type": "content"}
            )

            # Test accessing the document page with valid ID
            result = self.url_open(f"/knowledge/document/{document_page.id}")
            self.assertEqual(result.status_code, 200)

            # Test with an invalid document_page_id
            with self.assertRaises(MissingError):
                portal_controller = (
                    self.env["ir.http"]
                    .sudo()
                    ._get_class(
                        "odoo.addons.document_page_portal.controllers.portal.CustomerPortal"
                    )()
                )
                portal_controller._document_check_access("document.page", 999999)

            # Test access with an invalid token (simulating a public user access)
            with self.assertRaises(AccessError):
                portal_controller = (
                    self.env["ir.http"]
                    .sudo()
                    ._get_class(
                        "odoo.addons.document_page_portal.controllers.portal.CustomerPortal"
                    )()
                )
                portal_controller._document_check_access(
                    "document.page", document_page.id, access_token="invalid_token"
                )
