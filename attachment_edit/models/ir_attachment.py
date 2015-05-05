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


class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    res_reference = fields.Reference(
        selection='_selection_res_reference',
        string='Resource reference', compute='_compute_res_reference',
        inverse='_inverse_res_reference')

    @api.one
    @api.depends('res_id', 'res_model')
    def _compute_res_reference(self):
        if self.res_model and self.res_id:
            self.res_reference = '%s,%s' % (self.res_model, self.res_id)

    @api.one
    def _inverse_res_reference(self):
        if self.res_reference:
            self.write({
                'res_model': self.res_reference._model._model,
                'res_id': self.res_reference.id,
            })
        else:
            self.write({'res_model': False, 'res_id': False})

    @api.model
    def _selection_res_reference(self):
        return self.env['ir.model'].search([
            ('osv_memory', '=', False),
            ('access_ids.group_id.users', '=', self.env.uid)
        ]).mapped(lambda rec: (rec.model, rec.name))
