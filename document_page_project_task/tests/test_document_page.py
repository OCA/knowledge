# Copyright 2025 Marcel Savegnago - Escodoo <https://escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.exceptions import ValidationError
from odoo.tests import common


class TestDocumentPage(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.Page = cls.env["document.page"]
        cls.Project = cls.env["project.project"]
        cls.Task = cls.env["project.task"]

        cls.project1 = cls.Project.create({"name": "Project 1"})
        cls.project2 = cls.Project.create({"name": "Project 2"})
        cls.task1 = cls.Task.create({"name": "Task 1", "project_id": cls.project1.id})
        cls.task2 = cls.Task.create({"name": "Task 2", "project_id": cls.project2.id})
        cls.task3 = cls.Task.create({"name": "Task 3", "project_id": cls.project1.id})

    def test_onchange_task_ids_fills_project_single_project(self):
        """When all tasks share the same project, it is auto-filled."""
        page = self.Page.new({"name": "Test Page"})
        page.task_ids = self.task1 | self.task3
        page._onchange_task_ids()

        self.assertEqual(
            page.project_id,
            self.project1,
            "Project should be auto-filled when all tasks share the same project",
        )

    def test_onchange_task_ids_does_not_fill_project_multiple_projects(self):
        """When tasks span different projects, project is not auto-filled."""
        page = self.Page.new({"name": "Test Page"})
        page.task_ids = self.task1 | self.task2
        page._onchange_task_ids()

        self.assertFalse(
            page.project_id,
            "Project should not be auto-filled when tasks belong to different projects",
        )

    def test_onchange_task_ids_skips_when_project_already_set(self):
        """When project is already set, onchange does not overwrite it."""
        page = self.Page.new({"name": "Test Page", "project_id": self.project1.id})
        page.task_ids = self.task1
        page._onchange_task_ids()

        self.assertEqual(
            page.project_id,
            self.project1,
            "Existing project should not be overwritten by onchange",
        )

    def test_onchange_project_id_filters_incompatible_tasks(self):
        """When project changes, tasks not belonging to it are removed."""
        page = self.Page.new(
            {
                "name": "Test Page",
                "task_ids": [(4, self.task1.id), (4, self.task2.id)],
            }
        )
        page.project_id = self.project1
        page._onchange_project_id()

        self.assertIn(self.task1.id, page.task_ids.ids)
        self.assertNotIn(
            self.task2.id,
            page.task_ids.ids,
            "Task from a different project should be removed after project change",
        )

    def test_onchange_project_id_keeps_compatible_tasks(self):
        """Tasks already belonging to the selected project are kept."""
        page = self.Page.new(
            {
                "name": "Test Page",
                "project_id": self.project1.id,
                "task_ids": [(4, self.task1.id), (4, self.task3.id)],
            }
        )
        page._onchange_project_id()

        self.assertIn(self.task1.id, page.task_ids.ids)
        self.assertIn(self.task3.id, page.task_ids.ids)

    def test_onchange_project_cleared_keeps_tasks(self):
        """Clearing the project does not remove linked tasks."""
        page = self.Page.new(
            {
                "name": "Test Page",
                "project_id": self.project1.id,
                "task_ids": [(4, self.task1.id)],
            }
        )
        page.project_id = False
        page._onchange_project_id()

        self.assertIn(
            self.task1.id,
            page.task_ids.ids,
            "Tasks should be kept when project is cleared",
        )

    def test_default_get_with_task_in_context(self):
        """default_get fills task_ids and project_id from default_task_id context."""
        context = {"default_task_id": self.task1.id}
        fields_list = ["name", "project_id", "task_ids"]
        defaults = self.Page.with_context(**context).default_get(fields_list)

        self.assertEqual(
            defaults.get("project_id"),
            self.project1.id,
            "project_id should be filled from the context task's project",
        )
        self.assertIn(
            (4, self.task1.id),
            defaults.get("task_ids", []),
            "task_ids should contain the task from context",
        )

    def test_constraint_valid_tasks_same_project(self):
        """Creating a page with tasks all from the same project is allowed."""
        page = self.Page.create(
            {
                "name": "Test Page",
                "project_id": self.project1.id,
                "task_ids": [(4, self.task1.id), (4, self.task3.id)],
            }
        )
        self.assertTrue(page.exists())

    def test_constraint_invalid_task_different_project(self):
        """Linking a task from a different project raises ValidationError."""
        with self.assertRaises(ValidationError):
            self.Page.create(
                {
                    "name": "Test Page",
                    "project_id": self.project1.id,
                    "task_ids": [(4, self.task2.id)],
                }
            )

    def test_constraint_no_project_allows_any_tasks(self):
        """Without project_id, tasks from any project can be linked."""
        page = self.Page.create(
            {
                "name": "Test Page",
                "task_ids": [(4, self.task1.id), (4, self.task2.id)],
            }
        )
        self.assertTrue(page.exists())

    def test_constraint_no_tasks_no_project(self):
        """A page with no tasks and no project is valid."""
        page = self.Page.create({"name": "Test Page"})
        self.assertTrue(page.exists())

    def test_write_adding_incompatible_task_raises(self):
        """Writing a task from a different project raises ValidationError."""
        page = self.Page.create(
            {
                "name": "Test Page",
                "project_id": self.project1.id,
                "task_ids": [(4, self.task1.id)],
            }
        )
        with self.assertRaises(ValidationError):
            page.write({"task_ids": [(4, self.task2.id)]})

    def test_create_page_with_multiple_tasks_same_project(self):
        """A page can be linked to multiple tasks from the same project."""
        page = self.Page.create(
            {
                "name": "Test Page",
                "project_id": self.project1.id,
                "task_ids": [(4, self.task1.id), (4, self.task3.id)],
            }
        )
        self.assertEqual(len(page.task_ids), 2)
        self.assertIn(self.task1, page.task_ids)
        self.assertIn(self.task3, page.task_ids)
