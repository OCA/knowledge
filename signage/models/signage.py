# Copyright (C) 2025 Dimitrios Tanis (<dtanis@tanisfood.gr>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models
from odoo.tools.mail import html2plaintext


class Signage(models.Model):
    _name = "signage"
    _description = "Warning, obligation and information signs"

    @api.depends("name")
    def _compute_display_name(self):
        for record in self:
            record.display_name = html2plaintext(record.name)

    name = fields.Html(
        sanitize_style=True,
        required=True,
    )
    description = fields.Text()
    image = fields.Binary(
        attachment=True, help="This field holds the image used for the signage."
    )
    category_id = fields.Many2one(
        "signage.category",
        group_expand="_read_group_stage_ids",
    )

    @api.model
    def _read_group_stage_ids(self, stages, domain):
        """Show always the stages not folded."""
        search_domain = [
            ("fold", "=", False),
        ]
        return stages.search(search_domain)
