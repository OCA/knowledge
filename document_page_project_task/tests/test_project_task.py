# Copyright 2025 Marcel Savegnago - Escodoo <https://escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests import common


class TestProjectTask(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.Page = cls.env["document.page"]
        cls.Project = cls.env["project.project"]
        cls.Task = cls.env["project.task"]

        cls.project = cls.Project.create({"name": "Test Project"})
        cls.task = cls.Task.create({"name": "Test Task", "project_id": cls.project.id})
        cls.default_page = cls.Page.create({"name": "My page"})

    def test_page_count(self):
        """Page counter starts at zero and increments when a page is linked."""
        self.assertEqual(
            self.task.document_page_count,
            0,
            "Initial page count should be zero",
        )

        self.default_page.write(
            {
                "project_id": self.task.project_id.id,
                "task_ids": [(4, self.task.id)],
            }
        )
        self.task._compute_document_page_count()

        self.assertEqual(
            self.task.document_page_count,
            1,
            "After linking a page to the task, count should be one",
        )
        self.assertIn(
            self.default_page,
            self.task.document_page_ids,
            "The page should appear in the task's document_page_ids",
        )

    def test_page_count_multiple_pages(self):
        """Counter reflects the correct total when multiple pages are linked."""
        page2 = self.Page.create(
            {
                "name": "Second page",
                "project_id": self.task.project_id.id,
                "task_ids": [(4, self.task.id)],
            }
        )
        page3 = self.Page.create(
            {
                "name": "Third page",
                "project_id": self.task.project_id.id,
                "task_ids": [(4, self.task.id)],
            }
        )

        self.task._compute_document_page_count()

        self.assertEqual(
            self.task.document_page_count,
            2,
            "Count should be two with two pages associated",
        )
        self.assertIn(page2, self.task.document_page_ids)
        self.assertIn(page3, self.task.document_page_ids)

    def test_page_linked_to_multiple_tasks(self):
        """A single page can be linked to multiple tasks via M2M."""
        task2 = self.Task.create({"name": "Task 2", "project_id": self.project.id})
        page = self.Page.create(
            {
                "name": "Shared page",
                "project_id": self.project.id,
                "task_ids": [(4, self.task.id), (4, task2.id)],
            }
        )

        self.assertIn(page, self.task.document_page_ids)
        self.assertIn(page, task2.document_page_ids)
        self.assertEqual(len(page.task_ids), 2)
