# Copyright 2019 Creu Blanca
# Copyright 2025 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import re

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class DocumentPage(models.Model):
    _inherit = "document.page"
    _description = "Document Page"

    reference = fields.Char(
        help="Used to find the document, it can contain letters, numbers and _"
    )

    @api.constrains("reference")
    def _check_reference_validity(self):
        for rec in self:
            if not rec.reference:
                continue
            regex = r"^[a-zA-Z_][a-zA-Z0-9_]*$"
            if not re.match(regex, rec.reference):
                raise ValidationError(self.env._("Reference is not valid"))
            domain = [("reference", "=", rec.reference), ("id", "!=", rec.id)]
            if self.search(domain):
                raise ValidationError(self.env._("Reference must be unique"))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get("reference") and vals.get("name"):
                reference = self.env["ir.http"]._slugify(vals["name"]).replace("-", "_")
                vals["reference"] = reference
        return super().create(vals_list)
