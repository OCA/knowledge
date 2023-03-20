# Copyright 2019 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProjectProject(models.Model):
    _inherit = "project.project"

    document_page_ids = fields.One2many(
        string="Wiki",
        comodel_name="document.page",
        inverse_name="project_id",
        groups="knowledge.group_document_user",
    )

    document_page_count = fields.Integer(
        compute="_compute_document_page_count",
        groups="knowledge.group_document_user",
    )

    def _compute_document_page_count(self):
        for rec in self:
            rec.document_page_count = len(rec.document_page_ids)
