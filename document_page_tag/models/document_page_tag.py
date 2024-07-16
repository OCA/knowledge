# Copyright 2015-2018 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class DocumentPageTag(models.Model):
    _name = "document.page.tag"
    _description = "A keyword for document pages"

    name = fields.Char(required=True, translate=True)
    color = fields.Integer(string="Color Index")
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ("unique_name", "unique(name)", "Tags must be unique"),
    ]

    @api.model_create_multi
    def create(self, vals_list):
        """Be nice when trying to create duplicates"""
        for vals in vals_list:
            existing = self.search([("name", "=ilike", vals["name"])], limit=1)
            if existing:
                vals_list.remove(vals)
                if not vals_list:
                    return existing
        return super().create(vals_list)
