# -*- coding: utf-8 -*-
# © 2017 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import api, fields, models, tools


class IrActionsActWindow(models.Model):
    _inherit = 'ir.actions.act_window'

    enduser_help = fields.Html(compute='_compute_enduser_help', store=True)
    advanced_help = fields.Html(compute='_compute_advanced_help', store=True)
    enduser_document_page_ids = fields.Many2many(
        'document.page', 'help_popup_document_page_rel',
        'action_id', 'document_page_id',
        string='Documentation'
    )
    advanced_document_page_ids = fields.Many2many(
        'document.page', 'help_popup_document_page_advanced_rel',
        'action_id', 'document_page_id',
        string='Advanced documentation'
    )

    @api.multi
    @api.depends('enduser_document_page_ids.content')
    def _compute_enduser_help(self):
        for this in self:
            html_string = this.enduser_document_page_ids[:1].content
            for extra_content in this.enduser_document_page_ids[1:]:
                html_string = tools.append_content_to_html(
                    html_string, extra_content.content, plaintext=False
                )
            this.enduser_help = html_string

    @api.multi
    @api.depends('advanced_document_page_ids.content')
    def _compute_advanced_help(self):
        for this in self:
            html_string = this.advanced_document_page_ids[:1].content
            for extra_content in this.advanced_document_page_ids[1:]:
                html_string = tools.append_content_to_html(
                    html_string, extra_content.content, plaintext=False
                )
            this.advanced_help = html_string
