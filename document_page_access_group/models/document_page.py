# Copyright 2022 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class DocumentPage(models.Model):
    _inherit = "document.page"

    groups_id = fields.Many2many(comodel_name="res.groups", string="Groups")
