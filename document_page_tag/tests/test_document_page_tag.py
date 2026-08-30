# Copyright 2015-2018 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from psycopg2 import IntegrityError

from odoo.exceptions import UserError
from odoo.tests.common import TransactionCase
from odoo.tools.misc import mute_logger


class TestDocumentPageTag(TransactionCase):
    def test_document_page_tag(self):
        testtag = self.env["document.page.tag"].name_create("test")
        # check we're charitable on duplicates
        self.assertEqual(
            testtag,
            self.env["document.page.tag"].name_create("Test"),
        )
        # check we can't create nonunique tags
        with self.assertRaises(IntegrityError):
            with mute_logger("odoo.sql_db"):
                testtag2 = self.env["document.page.tag"].create({"name": "test2"})
                testtag2.write({"name": "test"})
                testtag2.flush_model()

    def test_document_page_tag_recursion(self):
        tag_a = self.env["document.page.tag"].create({"name": "tag a"})
        tag_b = self.env["document.page.tag"].create(
            {"name": "tag b", "parent_id": tag_a.id}
        )
        # native anti-recursion check from _parent_store
        with self.assertRaises(UserError):
            tag_a.parent_id = tag_b.id

    def test_document_page_tag_display_name_hierarchy(self):
        tag_a = self.env["document.page.tag"].create({"name": "tag a"})
        tag_b = self.env["document.page.tag"].create(
            {"name": "tag b", "parent_id": tag_a.id}
        )
        self.assertEqual(tag_b.display_name, "tag a / tag b")

    def test_document_page_tag_search_display_name(self):
        tag_a = self.env["document.page.tag"].create({"name": "tag a"})
        tag_b = self.env["document.page.tag"].create(
            {"name": "tag b", "parent_id": tag_a.id}
        )
        found = self.env["document.page.tag"].search(
            [("display_name", "ilike", "tag a")]
        )
        self.assertIn(tag_a, found)
        self.assertIn(tag_b, found)

    def test_document_page_tag_search_display_name_exact(self):
        # covers the non-"like" operator branch (no child_of expansion)
        tag_a = self.env["document.page.tag"].create({"name": "tag a"})
        found = self.env["document.page.tag"].search([("display_name", "=", "tag a")])
        self.assertEqual(found, tag_a)
