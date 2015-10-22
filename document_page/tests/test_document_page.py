# -*- coding: utf-8 -*-

from openerp.tests import common


class TestDocumentPage(common.TransactionCase):
    """document_page test class."""

    def test_page_creation(self):
        """Test page creation."""
        parent_page = self.env.ref('document_page.demo_category1')

        self.assertEqual(parent_page.name, 'OpenERP Features')

        record = self.env['document.page'].create({
            'name': 'Test Page1',
            'parent_id': parent_page.id,
            'content': 'Test content'
        })
        self.assertEqual(record.name, 'Test Page1')

    def test_category_display_content(self):
        """Test category display content."""
        page = self.env.ref('document_page.demo_category1')
        self.assertTrue(page.display_content.find('Demo') > 1)

    def test_page_display_content(self):
        """Test page display content."""
        page = self.env.ref('document_page.demo_page1')
        self.assertTrue(page.display_content.find('Demo') > 1)

    def test_page_do_set_content(self):
        """Test page set content."""
        page = self.env.ref('document_page.demo_page1')
        page.content = None
        page.do_set_content()
        self.assertTrue(page.display_content.find('Summary') == 1)
