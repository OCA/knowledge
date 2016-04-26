# -*- coding: utf-8 -*-
# © 2015 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# -*- coding: utf-8 -*-
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
