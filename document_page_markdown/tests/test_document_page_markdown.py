# Copyright 2026 Escodoo
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestDocumentPageMarkdown(TransactionCase):
    def setUp(self):
        super().setUp()
        self.page = self.env["document.page"]

    def test_render_headings_and_lists(self):
        html = self.page.render_markdown("# Title\n\n- first\n- second")
        self.assertIn("<h1>Title</h1>", html)
        self.assertIn("<li>first</li>", html)

    def test_render_inline_formatting(self):
        html = self.page.render_markdown("Some *text* and `code`.")
        self.assertIn("<em>text</em>", html)
        self.assertIn("<code>code</code>", html)

    def test_render_table(self):
        html = self.page.render_markdown("| A | B |\n| --- | --- |\n| 1 | 2 |")
        self.assertIn("<table>", html)

    def test_render_empty_source(self):
        self.assertEqual(self.page.render_markdown(""), "")
