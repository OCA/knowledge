# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.exceptions import AccessError
from odoo.tests import Form

from odoo.addons.base.tests.common import BaseCommon


class TestDocumentPage(BaseCommon):
    _test_user_groups = ("document_page.group_document_manager",)

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.page_obj = cls.env["document.page"]
        cls.history_obj = cls.env["document.page.history"]
        cls.category1 = cls.page_obj.create(
            {
                "name": "Odoo Features",
                "type": "category",
                "template": (
                    "\nSummary of the feature\n\n"
                    "Long explanation\n\n"
                    "Conclusion\n\n"
                    "Additional ressources\n\n"
                ),
            }
        )
        cls.page1 = cls.page_obj.create(
            {
                "name": "Odoo 15.0 Functional Demo",
                "parent_id": cls.category1.id,
                "content": "Test Content",
                "draft_name": "1.0",
                "draft_summary": "Init",
            }
        )

    def test_page_creation(self):
        page = self.page_obj.create(
            {
                "name": "Test Page 1",
                "parent_id": self.category1.id,
                "content": "<p>Test content</p>",
            }
        )
        self.assertEqual(page.content, "<p>Test content</p>")
        self.assertEqual(len(page.history_ids), 1)
        page.content = "<p>New content for Demo Page</p>"
        self.assertEqual(len(page.history_ids), 2)

    def test_page_edit_keeps_new_content(self):
        page = self.page_obj.create(
            {
                "name": "Test Page 2",
                "parent_id": self.category1.id,
                "content": "<p>v1</p>",
            }
        )
        page.write({"content": "<p>v2</p>"})
        self.env.flush_all()
        self.env.invalidate_all()
        self.assertEqual(page.history_head, page.history_ids.sorted("id")[-1])
        self.assertEqual(page.content, "<p>v2</p>")

    def test_category_template(self):
        page = self.page_obj.create(
            {"name": "Test Page 2", "parent_id": self.category1.id}
        )
        page._onchange_parent_id()
        self.assertEqual(page.content, self.category1.template)

    def test_page_history_diff(self):
        page = self.page_obj.create(
            {"name": "Test Page 3", "content": "<div>Test content</div>"}
        )
        page.content = "<div>New content</div>"
        self.assertIsNotNone(page.history_ids[0].diff)

    def test_page_link(self):
        page = self.page_obj.create(
            {"name": "Test Page 3", "content": "<div>Test content</div>"}
        )
        self.assertEqual(
            page.backend_url,
            f"/web#id={page.id}&model=document.page&view_type=form",
        )
        menu = self.env.ref("document_knowledge.menu_document")
        page.menu_id = menu
        self.assertEqual(
            page.backend_url,
            f"/web#id={page.id}&model=document.page&view_type=form&action={menu.action.id}",
        )

    def test_open_folder_unreadable_parent(self):
        other_company = self._create_company(name="Other company")
        pages = self.page_obj.sudo()
        hidden_root = pages.create(
            {
                "name": "Root folder of the other company",
                "type": "category",
                "company_id": other_company.id,
            }
        )
        hidden_folder = pages.create(
            {
                "name": "Folder of the other company",
                "type": "category",
                "parent_id": hidden_root.id,
                "company_id": other_company.id,
            }
        )
        shared_folder = pages.create(
            {
                "name": "Folder shared by all companies",
                "type": "category",
                "parent_id": hidden_folder.id,
                "company_id": False,
            }
        )
        pages.create(
            {
                "name": "Page of my company",
                "parent_id": shared_folder.id,
                "company_id": self.env.company.id,
                "content": "<p>Content</p>",
            }
        )
        pages.create(
            {
                "name": "Page of the other company",
                "parent_id": shared_folder.id,
                "company_id": other_company.id,
                "content": "<p>Content</p>",
            }
        )
        self.env.flush_all()
        self.env.invalidate_all()
        with self.assertRaises(AccessError):
            hidden_folder.with_env(self.env).read(["name"])
        folder_form = Form(
            shared_folder.with_env(self.env), view="document_page.view_category_form"
        )
        self.assertIn("Page of my company", folder_form.content)
        self.assertNotIn("Page of the other company", folder_form.content)

    def test_page_copy(self):
        page = self.page_obj.create(
            {"name": "Test Page 3", "content": "<div>Test content</div>"}
        )
        page_copy = page.copy()
        self.assertEqual(page_copy.name, page.name + " (copy)")
        self.assertEqual(page_copy.content, page.content)
        self.assertEqual(page_copy.draft_name, "1.0")
        self.assertEqual(page_copy.draft_summary, "summary")
