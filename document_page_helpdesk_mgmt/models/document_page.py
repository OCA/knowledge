# Copyright 2026 - TODAY, Cristiano Mafra Junior <cristiano.mafra@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class DocumentPage(models.Model):
    _inherit = "document.page"

    helpdesk_ticket_ids = fields.Many2many(
        string="Helpdesk Tickets",
        comodel_name="helpdesk.ticket",
        relation="document_page_helpdesk_ticket_rel",
        column1="document_page_id",
        column2="helpdesk_ticket_id",
    )
