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

    @api.multi
    @api.depends('res_id', 'res_model')
    def _compute_res_reference(self):
        for this in self:
            if this.res_model and this.res_id:
                this.res_reference = '%s,%s' % (this.res_model, this.res_id)

    @api.multi
    def _inverse_res_reference(self):
        for this in self:
            if this.res_reference:
                this.write({
                    'res_model': this.res_reference._name,
                    'res_id': this.res_reference.id,
                })
            else:
                this.write({'res_model': False, 'res_id': False})

    @api.model
    def _selection_res_reference(self):
        return self.env['ir.model'].search([
            ('transient', '=', False),
            ('access_ids.group_id.users', '=', self.env.uid)
        ]).mapped(lambda rec: (rec.model, rec.name))
