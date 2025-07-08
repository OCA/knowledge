# Copyright 2025 Juan Alberto Raja<juan.raja@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class DocumentPage(models.Model):
    _inherit = "document.page"

    is_not_printable = fields.Boolean(
        compute="_compute_is_not_printable",
        store=True,
        help="Indicates if the document cannot be printed based on its tags",
    )

    @api.depends("tag_ids", "tag_ids.is_not_printable")
    def _compute_is_not_printable(self):
        for record in self:
            record.is_not_printable = any(
                tag.is_not_printable for tag in record.tag_ids
            )
