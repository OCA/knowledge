# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class DocumentPageReferenceRule(models.Model):

    _name = 'document.page.reference.rule'
    _description = 'Document Page Reference Rule'

    name = fields.Char(required=True)
    model_id = fields.Many2one('ir.model')
    model_name = fields.Char(readonly=True, related='model_id.model')
    field_id = fields.Many2one('ir.model.fields')
    extra_domain = fields.Char(default='[]')
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "This name already exists !"),
    ]

    @api.onchange('model_id')
    def onchange_model(self):
        self.field_id = False
