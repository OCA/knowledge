# -*- coding: utf-8 -*-
# © 2017 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import fields, models


class DocumentPage(models.Model):
    _inherit = 'document.page'

    help_popup_window_action_ids = fields.Many2many(
        'ir.actions.act_window', 'help_popup_document_page_rel',
        'document_page_id', 'action_id',
        string='Documentation for'
    )

    help_popup_window_advanced_action_ids = fields.Many2many(
        'ir.actions.act_window', 'help_popup_document_page_advanced_rel',
        'document_page_id', 'action_id',
        string='Advanced documentation for'
    )
