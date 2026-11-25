# Copyright (C) 2025 Dimitrios Tanis (<dtanis@tanisfood.gr>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class SignageCategory(models.Model):
    _name = "signage.category"
    _description = "Category for signs"

    name = fields.Char(
        "Category Name",
        required=True,
    )
    description = fields.Text()
    signage_ids = fields.One2many(
        comodel_name="signage",
        inverse_name="category_id",
        string="Signage",
    )
    sequence = fields.Integer(default=1)
    fold = fields.Boolean(
        string="Folded in Kanban",
        help="This stage is folded in the kanban view "
        "when there are no records in that stage "
        "to display.",
    )
    font_color_hex = fields.Char(
        "Font Color Code",
        default=False,
        help="Color code in Hex, # (pound sign) included",
    )
    background_color_hex = fields.Char(
        "Background Color Code",
        default=False,
        help="Color code in Hex used for background, # (pound sign) included",
    )
