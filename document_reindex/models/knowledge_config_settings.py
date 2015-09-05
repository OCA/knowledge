# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2015 Therp BV (<http://therp.nl>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp import models, fields, api


class KnowledgeConfigSettings(models.TransientModel):
    _inherit = 'knowledge.config.settings'

    document_reindex_all = fields.Boolean('Reindex all documents')
    document_reindex_unindexed = fields.Boolean('Reindex unindexed documents')

    @api.one
    def set_document_reindex(self):
        if self.document_reindex_all:
            self.document_reindex_create_cronjob('document_reindex_all')
        if self.document_reindex_unindexed:
            self.document_reindex_create_cronjob('document_reindex_unindexed')

    @api.multi
    def document_reindex_create_cronjob(self, function):
        self.env['ir.cron'].create({
            'name': function,
            'model': 'ir.attachment',
            'function': function,
        })
