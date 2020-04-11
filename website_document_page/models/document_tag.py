# Copyright (C) 2020 Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class DocumentTag(models.Model):
    _inherit = "document.tag"
    _order = "sequence"

    is_menu = fields.Boolean("Show in the Wiki menu")
    sequence = fields.Integer("Sequence")
