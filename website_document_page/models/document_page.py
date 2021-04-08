# Copyright (C) 2020 Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class DocumentPage(models.Model):
    _inherit = [
        "document.page",
        "website.seo.metadata",
        "website.published.multi.mixin",
    ]
    _name = "document.page"
    _order = "sequence"

    is_menu = fields.Boolean("Show in the Wiki menu")
    sequence = fields.Integer("Sequence")
