# Copyright 2025 Marcel Savegnago - Escodoo <https://escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class DocumentPage(models.Model):
    _inherit = "document.page"

    task_ids = fields.Many2many(
        string="Tasks",
        comodel_name="project.task",
        relation="document_page_project_task_rel",
        column1="document_page_id",
        column2="task_id",
    )

    @api.onchange("task_ids")
    def _onchange_task_ids(self):
        """If no project is set and all tasks share the same project, fill it."""
        if self.task_ids and not self.project_id:
            projects = self.task_ids.mapped("project_id")
            if len(projects) == 1:
                self.project_id = projects

    @api.onchange("project_id")
    def _onchange_project_id(self):
        """Remove tasks that don't belong to the newly selected project."""
        if self.project_id and self.task_ids:
            self.task_ids = self.task_ids.filtered(
                lambda t: t.project_id == self.project_id
            )

    @api.constrains("task_ids", "project_id")
    def _check_task_project_consistency(self):
        """Ensure all linked tasks belong to the document's project."""
        for record in self:
            if record.project_id and record.task_ids:
                invalid_tasks = record.task_ids.filtered(
                    lambda t, r=record: t.project_id != r.project_id
                )
                if invalid_tasks:
                    raise ValidationError(
                        _(
                            "All linked tasks must belong to the document's project "
                            "'%(project)s'. The following tasks belong to a different "
                            "project: %(tasks)s.",
                            project=record.project_id.name,
                            tasks=", ".join(invalid_tasks.mapped("name")),
                        )
                    )

    @api.model
    def default_get(self, fields_list):
        """Fill task_ids and project_id when created with default_task_id in context."""
        res = super().default_get(fields_list)
        if "default_task_id" in self.env.context:
            task = self.env["project.task"].browse(
                self.env.context.get("default_task_id")
            )
            if task.exists():
                if "task_ids" in fields_list:
                    res["task_ids"] = [(4, task.id)]
                if "project_id" in fields_list and task.project_id:
                    res["project_id"] = task.project_id.id
        return res
