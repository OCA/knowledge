# -*- coding: utf-8 -*-
from openerp.tests import common


class TestDocumentPageApproval(common.TransactionCase):
    """Test document page approval model."""

    def test_get_display_content(self):
        """Test page display content."""
        # Check content of a category
        category = self.env['document.page'].search([
            ('name', '=', 'OpenERP Features')
            ])

        self.assertIsNotNone(category.display_content, 'a category')

        # Check content of a page
        pages = self.env['document.page'].search([
            ('parent_id', '=', category.id)
            ])
        page = pages[0]
        self.assertIsNotNone(page.display_content, 'Page content')

        # Check if approval is required
        self.assertFalse(page.is_approval_required(page))

        # Check content of an approval page
        page.approval_required = True

        self.assertIsNotNone(page.display_content, 'Page content')

        # Check if approval is required
        self.assertTrue(page.is_approval_required(page))

        # Check if parent approval is required
        self.assertTrue(page.is_parent_approval_required)
