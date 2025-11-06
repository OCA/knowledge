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
        """Test the page counter on the task."""
        self.assertEqual(
            self.task.document_page_count,
            0,
            "Initial page count should be zero",
        )

        # Set task_id and project_id together (the onchange fills project_id)
        self.default_page.write(
            {"task_id": self.task.id, "project_id": self.task.project_id.id}
        )
        self.task._compute_document_page_count()

        self.assertEqual(
            self.task.document_page_count,
            1,
            "After associating task to document, the count should be one",
        )
        self.assertIn(
            self.default_page,
            self.task.document_page_ids,
            "The page should be in the list of document pages for the task",
        )

    def test_page_count_multiple_pages(self):
        """Test the counter with multiple pages."""
        page2 = self.Page.create(
            {
                "name": "Second page",
                "task_id": self.task.id,
                "project_id": self.task.project_id.id,
            }
        )
        page3 = self.Page.create(
            {
                "name": "Third page",
                "task_id": self.task.id,
                "project_id": self.task.project_id.id,
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
