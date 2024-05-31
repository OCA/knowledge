# Copyright 2024 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class DocumentPage(models.Model):
    _inherit = "document.page"

    groups_id = fields.Many2many(compute="_compute_groups_id", store=True)
    role_ids = fields.Many2many(
        comodel_name="res.users.role",
        relation="document_page_user_roles_rel",
        column1="page_id",
        column2="role_id",
        string="Roles",
    )

    @api.depends("role_ids", "role_ids.implied_ids")
    def _compute_groups_id(self):
        """Create a compute to auto-set all the groups of the related roles."""
        for item in self:
            item.groups_id = item.mapped("role_ids.implied_ids")
