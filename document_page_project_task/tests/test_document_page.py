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

    def test_onchange_task_id_fills_project(self):
        """Test that when selecting a task, the project is automatically
        filled."""
        page = self.Page.new({"name": "Test Page"})
        page.task_id = self.task1
        page._onchange_task_id()

        self.assertEqual(
            page.project_id,
            self.project1,
            "The project should be automatically filled with the task's project",
        )

    def test_onchange_project_id_clears_task(self):
        """Test that when changing the project to a different one, the task
        is cleared."""
        page = self.Page.new(
            {
                "name": "Test Page",
                "task_id": self.task1.id,
                "project_id": self.project1.id,
            }
        )
        page.project_id = self.project2
        page._onchange_project_id()

        self.assertFalse(
            page.task_id,
            "The task should be cleared when the project changes to a different one",
        )

    def test_onchange_project_id_clears_task_when_removed(self):
        """Test that when removing the project, the task is cleared."""
        page = self.Page.new(
            {
                "name": "Test Page",
                "task_id": self.task1.id,
                "project_id": self.project1.id,
            }
        )
        page.project_id = False
        page._onchange_project_id()

        self.assertFalse(
            page.task_id,
            "The task should be cleared when the project is removed",
        )

    def test_default_get_with_task_in_context(self):
        """Test that default_get fills the project when there is default_task_id
        in the context."""
        context = {"default_task_id": self.task1.id}
        fields_list = ["name", "project_id", "task_id"]
        defaults = self.Page.with_context(**context).default_get(fields_list)

        self.assertEqual(
            defaults.get("project_id"),
            self.project1.id,
            "The project_id should be filled with the task's project in context",
        )
        self.assertEqual(
            defaults.get("task_id"),
            self.task1.id,
            "The task_id should be filled with the task from context",
        )

    def test_constraint_task_project_consistency_valid(self):
        """Test that the constraint allows task and project from the same
        project."""
        page = self.Page.create(
            {
                "name": "Test Page",
                "task_id": self.task1.id,
                "project_id": self.project1.id,
            }
        )

        # Should not raise an exception
        self.assertTrue(page.exists())

    def test_constraint_task_project_consistency_invalid(self):
        """Test that the constraint prevents task and project from different
        projects."""
        page = self.Page.create(
            {
                "name": "Test Page",
                "task_id": self.task1.id,
                "project_id": self.project1.id,
            }
        )

        # Trying to change the project to a different one should raise
        # ValidationError
        with self.assertRaises(ValidationError):
            page.project_id = self.project2

    def test_constraint_task_project_consistency_no_task(self):
        """Test that the constraint does not prevent when there is no task."""
        page = self.Page.create({"name": "Test Page", "project_id": self.project1.id})

        # Should not raise an exception when there is no task
        self.assertTrue(page.exists())

    def test_constraint_task_project_consistency_no_project(self):
        """Test that the constraint prevents when there is a task but no
        project."""
        # Trying to create a page with a task but without a project should
        # raise ValidationError
        with self.assertRaises(ValidationError):
            self.Page.create({"name": "Test Page", "task_id": self.task1.id})

    def test_constraint_task_requires_project(self):
        """Test that when removing the project when there is a task, it should
        raise an error."""
        page = self.Page.create(
            {
                "name": "Test Page",
                "task_id": self.task1.id,
                "project_id": self.project1.id,
            }
        )

        # Trying to remove the project when there is a task should raise
        # ValidationError
        with self.assertRaises(ValidationError):
            page.project_id = False

    def test_create_page_with_task_sets_project(self):
        """Test that when creating a page with a task, the project is set
        automatically."""
        # Create page with task_id and project_id defined together
        # (the onchange fills the project_id when task_id is defined in the
        # form)
        page = self.Page.create(
            {
                "name": "Test Page",
                "task_id": self.task1.id,
                "project_id": self.project1.id,
            }
        )

        self.assertEqual(
            page.project_id,
            self.project1,
            "The project should be the same as the task",
        )
        self.assertEqual(
            page.task_id,
            self.task1,
            "The task should be correctly associated",
        )

    def test_write_task_changes_project(self):
        """Test that when changing the task, the project should be updated."""
        page = self.Page.create(
            {
                "name": "Test Page",
                "task_id": self.task1.id,
                "project_id": self.project1.id,
            }
        )

        # Change the task - the project should be updated to match
        page.write({"task_id": self.task2.id, "project_id": self.task2.project_id.id})

        page.invalidate_recordset()
        self.assertEqual(
            page.project_id,
            self.project2,
            "The project should match the new task's project",
        )
