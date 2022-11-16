# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestDocumentReference(TransactionCase):
    def setUp(self):
        super().setUp()
        self.page_obj = self.env["document.page"]
        self.history_obj = self.env["document.page.history"]
        self.page1 = self.page_obj.create(
            {"name": "Test Page 1", "content": "${r2}", "reference": "R1"}
        )
        self.page2 = self.page_obj.create(
            {"name": "Test Page 1", "content": "${r1}", "reference": "r2"}
        )

    def test_constrains_01(self):
        with self.assertRaises(ValidationError):
            self.page2.write({"reference": self.page1.reference})

    def test_constrains_02(self):
        with self.assertRaises(ValidationError):
            self.page2.write({"reference": self.page2.reference + "-02"})

    def test_no_contrains(self):
        self.page1.write({"reference": False})
        self.page2.write({"reference": False})
        self.assertEqual(self.page1.reference, self.page2.reference)

    def test_check_raw(self):
        self.assertEqual(self.page2.display_name, self.page1.get_raw_content())

    def test_check_reference(self):
        self.assertRegex(self.page1.content_parsed, ".*%s.*" % self.page2.display_name)

    def test_no_reference(self):
        self.page2.reference = "r3"
        self.assertRegex(self.page1.content_parsed, ".*r2.*")

    def test_auto_reference(self):
        """Test if reference is proposed when saving a page without one."""
        self.assertEqual(self.page1.reference, "R1")
        new_page = self.page_obj.create(
            {"name": "Test Page with no rEfErenCe", "content": "some content"}
        )
        self.assertEqual(new_page.reference, "test_page_with_no_reference")
        new_page_duplicated_name = self.page_obj.create(
            {
                "name": "test page with no reference",
                "content": "this should have an empty reference "
                "because reference must be unique",
            }
        )
        self.assertFalse(new_page_duplicated_name.reference)
