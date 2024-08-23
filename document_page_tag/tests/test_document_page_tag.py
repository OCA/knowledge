# Copyright 2015-2018 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from psycopg2 import IntegrityError

from odoo.tests.common import TransactionCase
from odoo.tools.misc import mute_logger


class TestDocumentPageTag(TransactionCase):
    def test_document_page_tag(self):
        test_tag = self.env["document.page.tag"].name_create("test")
        # check we're charitable on duplicates
        self.assertEqual(
            test_tag,
            self.env["document.page.tag"].name_create("Test"),
        )
        # check multiple record creation
        test_tag1 = self.env["document.page.tag"].create(
            [{"name": "test1"}, {"name": "test"}, {"name": "test2"}]
        )
        self.assertEqual(len(test_tag1), 2)
        self.assertEqual(test_tag1[0].name, "test1")
        self.assertEqual(test_tag1[1].name, "test2")

        # check single record creation where record already exist
        test_tag2 = self.env["document.page.tag"].create([{"name": "test"}])
        self.assertEqual(len(test_tag2), 1)
        self.assertEqual(test_tag2[0].name, "test")

        # check we can't create nonunique tags
        with self.assertRaises(IntegrityError):
            with mute_logger("odoo.sql_db"):
                test_tag3 = self.env["document.page.tag"].create([{"name": "test3"}])
                test_tag3.write({"name": "test"})
                test_tag3.flush_model()
