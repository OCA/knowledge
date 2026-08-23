# Copyright 2026 - TODAY, Cristiano Mafra Junior <cristiano.mafra@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class HelpdeskTicket(models.Model):
    _inherit = "helpdesk.ticket"

    document_page_ids = fields.Many2many(
        string="Wiki",
        comodel_name="document.page",
        relation="document_page_helpdesk_ticket_rel",
        column1="helpdesk_ticket_id",
        column2="document_page_id",
    )
    document_page_count = fields.Integer(compute="_compute_document_page_count")

    def _compute_document_page_count(self):
        for rec in self:
            rec.document_page_count = len(rec.document_page_ids)
