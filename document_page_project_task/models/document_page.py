# Copyright 2025 Marcel Savegnago - Escodoo <https://escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class DocumentPage(models.Model):
    _inherit = "document.page"

    task_id = fields.Many2one(string="Task", comodel_name="project.task")

    @api.onchange("task_id")
    def _onchange_task_id(self):
        """Fill the project_id field with the task's related project."""
        if self.task_id and self.task_id.project_id:
            self.project_id = self.task_id.project_id

    @api.onchange("project_id")
    def _onchange_project_id(self):
        """Clear the task if the project is removed or changed and does not
        match the task's project."""
        if self.task_id:
            if not self.project_id or self.task_id.project_id != self.project_id:
                self.task_id = False

    @api.constrains("task_id", "project_id")
    def _check_task_project_consistency(self):
        """Ensure that the project is the same as the task's project when a
        task is defined."""
        for record in self:
            # If there is a task, there must be a project
            if record.task_id and not record.project_id:
                raise ValidationError(
                    _(
                        "When a task is linked, the project must be defined. "
                        "Task '%(task)s' requires that the project be defined.",
                        task=record.task_id.name,
                    )
                )
            # If there is a task and project, they must be from the same project
            if record.task_id and record.project_id:
                if record.task_id.project_id != record.project_id:
                    raise ValidationError(
                        _(
                            "The wiki document's project must be the same as the "
                            "task's project. Task '%(task)s' belongs to project "
                            "'%(task_project)s', but the document is associated "
                            "with project '%(doc_project)s'.",
                            task=record.task_id.name,
                            task_project=record.task_id.project_id.name,
                            doc_project=record.project_id.name,
                        )
                    )

    @api.model
    def default_get(self, fields_list):
        """Fill the project_id when the wiki is created with default_task_id
        in the context."""
        res = super().default_get(fields_list)
        if "default_task_id" in self.env.context and "project_id" in fields_list:
            task = self.env["project.task"].browse(
                self.env.context.get("default_task_id")
            )
            if task.exists() and task.project_id:
                res["project_id"] = task.project_id.id
        return res
