# Copyright 2025 Marcel Savegnago - Escodoo <https://escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    document_page_ids = fields.Many2many(
        string="Wiki Pages",
        comodel_name="document.page",
        relation="document_page_project_task_rel",
        column1="task_id",
        column2="document_page_id",
    )
    document_page_count = fields.Integer(compute="_compute_document_page_count")

    @api.depends("document_page_ids")
    def _compute_document_page_count(self):
        for rec in self:
            rec.document_page_count = len(rec.document_page_ids)
