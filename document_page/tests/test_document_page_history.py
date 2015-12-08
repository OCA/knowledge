# -*- coding: utf-8 -*-

from openerp.tests import common


class TestDocumentPageHistory(common.TransactionCase):
    """document_page_history test class."""

    def test_page_history_demo_page1(self):
        """Test page history demo page1."""
        page = self.env.ref('document_page.demo_page1')
        page.content = 'Test content updated'
        history_document = self.env['document.page.history']
        history_pages = history_document.search([('page_id', '=', page.id)])
        history_document.with_context(
            active_ids=[i.id for i in history_pages]
        ).get_diff()
