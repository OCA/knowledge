# -*- coding: utf-8 -*-
# © 2017 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import _, api, fields, models
from openerp.exceptions import Warning as UserError


class KnowledgeConfigSettings(models.TransientModel):
    _inherit = 'knowledge.config.settings'

    document_wopi_client = fields.Char(
        'WOPI client', required=True,
        default=lambda self: self._default_document_wopi_client()
    )

    @api.multi
    def set_document_wopi_client(self):
        self.ensure_one()
        self.env['ir.config_parameter'].set_param(
            'document_wopi.client', self.document_wopi_client
        )
        self.env['document.wopi']._discovery.clear_cache(
            self.env['document.wopi']
        )
        response = self.env['document.wopi']._discovery()
        if not response:
            raise UserError(
                _("%s doesn't seem to support WOPI discovery") %
                self.document_wopi_client
            )

    @api.model
    def _default_document_wopi_client(self):
        return self.env['ir.config_parameter'].get_param(
            'document_wopi.client'
        )
