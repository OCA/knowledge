# Copyright 2020 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestAttachmentCategory(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.category_model = cls.env["ir.attachment.category"]
        cls.attachment_model = cls.env["ir.attachment"]

        # Create Categories
        cls.parent_category = cls.category_model.create({"name": "Parent Category"})
        cls.child_category = cls.category_model.create(
            {
                "name": "Child Category",
                "parent_id": cls.parent_category.id,
            }
        )

        # Create Attachments
        cls.attachment_1 = cls.attachment_model.create(
            {
                "name": "Attachment 1",
                "datas": b"R0lGODlhAQABAIAAAP///wAAACwAAAAAAQABAAACAkQBADs=",
                "category_ids": [(4, cls.parent_category.id)],
            }
        )
        cls.attachment_2 = cls.attachment_model.create(
            {
                "name": "Attachment 2",
                "datas": b"R0lGODlhAQABAIAAAP///wAAACwAAAAAAQABAAACAkQBADs=",
                "category_ids": [(4, cls.child_category.id)],
            }
        )

    def test_01_compute_complete_name(self):
        """Test the complete_name and display_name computation"""
        self.assertEqual(self.parent_category.complete_name, "Parent Category")
        self.assertEqual(self.parent_category.display_name, "Parent Category")

        self.assertEqual(
            self.child_category.complete_name, "Parent Category/Child Category"
        )
        self.assertEqual(
            self.child_category.display_name, "Parent Category/Child Category"
        )

    def test_02_compute_attachment_count(self):
        """Test attachment_count computation including child categories"""
        # Parent should count its own and its children's attachments
        self.assertEqual(self.parent_category.attachment_count, 2)
        self.assertIn(self.attachment_1, self.parent_category.attachment_ids)
        self.assertIn(self.attachment_2, self.parent_category.attachment_ids)

        # Child should count only its own
        self.assertEqual(self.child_category.attachment_count, 1)
        self.assertIn(self.attachment_2, self.child_category.attachment_ids)
        self.assertNotIn(self.attachment_1, self.child_category.attachment_ids)

    def test_03_new_record(self):
        """Test attachment_count on a new record in memory"""
        new_category = self.env["ir.attachment.category"].new({"name": "New Category"})
        # It should not crash and should return 0 attachments
        self.assertEqual(new_category.attachment_count, 0)

    def test_04_action_attachment_view(self):
        """Test the action_attachment_view method"""
        action = self.parent_category.action_attachment_view()
        self.assertIsInstance(action, dict)

        # Verify the domain
        domain = action.get("domain")
        self.assertTrue(domain)
        # In Odoo 19 domains are objects, so we check their string representation
        domain_str = str(domain)
        self.assertIn("category_ids", domain_str)
        self.assertIn("child_of", domain_str)
        self.assertIn(str(self.parent_category.id), domain_str)

        # Verify the context
        context = action.get("context", {})
        self.assertEqual(context.get("default_category_ids"), [self.parent_category.id])
