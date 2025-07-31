# Copyright 2025 Juan Alberto Raja<juan.raja@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models


class DocumentPageTag(models.Model):
    _inherit = "document.page.tag"

    is_not_printable = fields.Boolean(
        default=False,
        help="If checked, pages with this tag cannot be printed",
    )
