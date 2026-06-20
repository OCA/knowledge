# Copyright 2025 TRIVAX INNOVA SL
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpCase, tagged


@tagged("post_install", "-at_install")
class TestDocumentPageReferenceTour(HttpCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Ensure admin password is known for the tour
        cls.env["res.users"].browse(2).write({"password": "admin"})
        page_obj = cls.env["document.page"]
        # Create a category
        cls.category = page_obj.create(
            {
                "name": "Test Ref Category",
                "type": "category",
            }
        )
        # Create two pages with cross-references
        cls.page1 = page_obj.create(
            {
                "name": "Test Ref Page 1",
                "parent_id": cls.category.id,
                "content": "<p>Go to ${r2} for details.</p>",
                "reference": "r1",
            }
        )
        cls.page2 = page_obj.create(
            {
                "name": "Test Ref Page 2",
                "parent_id": cls.category.id,
                "content": "<p>Back to ${r1} for overview.</p>",
                "reference": "r2",
            }
        )

    def test_reference_widget_renders_links(self):
        """Test that the document_page_reference widget renders ${ref}
        as clickable links and navigates without opening new tabs."""
        self.start_tour(
            "/web#action=document_page.action_page",
            "document_page_reference_widget_tour",
            login="admin",
            timeout=60,
        )

    def test_category_index_links(self):
        """Test that category pages show child links as oe_direct_line
        without duplicating content."""
        self.start_tour(
            "/web#action=document_page.action_page",
            "document_page_reference_category_tour",
            login="admin",
            timeout=60,
        )
