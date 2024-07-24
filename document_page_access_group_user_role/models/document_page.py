# Copyright 2024 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class DocumentPage(models.Model):
    _inherit = "document.page"

    user_ids = fields.Many2many(compute="_compute_user_ids", store=True, readonly=False)
    role_ids = fields.Many2many(
        comodel_name="res.users.role",
        relation="document_page_user_roles_rel",
        column1="page_id",
        column2="role_id",
        string="Roles",
    )

    @api.depends("role_ids", "role_ids.users")
    def _compute_user_ids(self):
        """Create a compute to auto-set all the users of the related roles."""
        for item in self:
            item.user_ids += item.mapped("role_ids.users")
