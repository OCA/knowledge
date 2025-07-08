from odoo.exceptions import UserError
from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged("post_install", "-at_install")
class TestDocumentPrintControl(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.printable_tag = cls.env["document.page.tag"].create(
            {"name": "Printable", "is_not_printable": False}
        )
        cls.non_printable_tag = cls.env["document.page.tag"].create(
            {"name": "Non-Printable", "is_not_printable": True}
        )
        cls.doc_without_tags = cls.env["document.page"].create(
            {"name": "Document Without Tags", "content": "Content"}
        )
        cls.doc_printable = cls.env["document.page"].create(
            {
                "name": "Printable Document",
                "content": "Content",
                "tag_ids": [(4, cls.printable_tag.id)],
            }
        )
        cls.doc_non_printable = cls.env["document.page"].create(
            {
                "name": "Non-Printable Document",
                "content": "Content",
                "tag_ids": [(4, cls.non_printable_tag.id)],
            }
        )
        cls.doc_mixed_tags = cls.env["document.page"].create(
            {
                "name": "Mixed Tags Document",
                "content": "Content",
                "tag_ids": [(4, cls.printable_tag.id), (4, cls.non_printable_tag.id)],
            }
        )

    def test_document_without_tags_is_printable(self):
        """Document without tags is printable."""
        self.assertFalse(self.doc_without_tags.is_not_printable)

    def test_document_with_printable_tag(self):
        """Document with printable tag is printable."""
        self.assertFalse(self.doc_printable.is_not_printable)

    def test_document_with_non_printable_tag(self):
        """Document with non-printable tag is not printable."""
        self.assertTrue(self.doc_non_printable.is_not_printable)

    def test_document_with_mixed_tags(self):
        """Document with mixed tags is not printable."""
        self.assertTrue(self.doc_mixed_tags.is_not_printable)

    def test_report_non_printable_raises_error(self):
        """Report fails if all documents are non-printable."""
        with self.assertRaises(UserError) as ctx:
            self.env["report.document_page.report_documentpage"]._get_report_values(
                [self.doc_non_printable.id]
            )
        self.assertIn("None of the selected pages can be printed", str(ctx.exception))

    def test_report_mixed_docs_raises_error(self):
        """Report fails if some documents are non-printable."""
        with self.assertRaises(UserError) as ctx:
            self.env["report.document_page.report_documentpage"]._get_report_values(
                [self.doc_printable.id, self.doc_non_printable.id]
            )
        self.assertIn("Some pages cannot be printed", str(ctx.exception))
        self.assertIn(self.doc_non_printable.name, str(ctx.exception))

    def test_report_printable_docs(self):
        """Report returns correct values for printable documents."""
        values = self.env[
            "report.document_page.report_documentpage"
        ]._get_report_values([self.doc_printable.id])
        self.assertEqual(values["doc_ids"], [self.doc_printable.id])
        self.assertEqual(values["doc_model"], "document.page")
        self.assertEqual(values["docs"].ids, [self.doc_printable.id])

    def test_manager_bypasses_print_restrictions(self):
        """Manager can print any document."""
        self.env.user.groups_id |= self.env.ref("document_page.group_document_manager")
        values = self.env[
            "report.document_page.report_documentpage"
        ]._get_report_values([self.doc_non_printable.id])
        self.assertEqual(values["doc_ids"], [self.doc_non_printable.id])
