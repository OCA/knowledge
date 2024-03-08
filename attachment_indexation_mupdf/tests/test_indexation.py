# Copyright 2023 len-foss/Financial Way
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import os
from unittest import skipIf

from odoo.tests.common import TransactionCase, tagged

directory = os.path.dirname(__file__)

try:
    import fitz
except ImportError:
    fitz = None


@tagged("post_install", "-at_install")
class TestCaseIndexation(TransactionCase):
    @skipIf(fitz is None, "PyMyPDF is not installed")
    def test_attachment_pdf_indexation(self):
        with open(os.path.join(directory, "files", "test_content.pdf"), "rb") as file:
            pdf = file.read()
            text = self.env["ir.attachment"]._index(pdf, "application/pdf")
            # note that the whitespace character is not the same as with pdfminer
            self.assertEqual(
                text, "TestContent!!\n", "the index content should be correct"
            )
