# Copyright 2025 Juan Alberto Raja<juan.raja@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import _, api, models
from odoo.exceptions import UserError


class ReportDocumentPage(models.AbstractModel):
    _name = "report.document_page.report_documentpage"
    _description = "Document Page Report with Print Control"

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env["document.page"].browse(docids).exists()
        printable_docs = docs

        if not self.env.user.has_group("document_page.group_document_manager"):
            printable_docs = docs.filtered(lambda d: not d.is_not_printable)

            if not printable_docs:
                raise UserError(
                    _("None of the selected pages can be printed due to their tags.")
                )

            if len(printable_docs) < len(docs):
                non_printable = docs - printable_docs
                raise UserError(
                    _("Some pages cannot be printed due to their tags:\n")
                    + "\n".join(f"- {doc.name}" for doc in non_printable)
                )

        report_values = {
            "doc_ids": printable_docs.ids,
            "doc_model": "document.page",
            "docs": printable_docs,
        }

        return report_values
