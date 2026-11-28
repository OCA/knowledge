# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.exceptions import AccessError
from odoo.tests import common


class TestDocumentPage(common.TransactionCase):
    def setUp(self):
        super(TestDocumentPage, self).setUp()
        self.page_obj = self.env["document.page"]
        self.history_obj = self.env["document.page.history"]
        self.category1 = self.env.ref("document_page.demo_category1")
        self.page1 = self.env.ref("document_page.demo_page1")

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
        page.content = "New content for Demo Page"
        self.assertEqual(len(page.history_ids), 2)
        page.content = "Another new content for Demo Page"
        self.assertEqual(len(page.history_ids), 3)
        # ensure history head is the latest revision (default sort order is ID DESC)
        self.assertEqual(page.history_head.id, max(page.history_ids.ids))

    def test_category_template(self):
        page = self.page_obj.create(
            {"name": "Test Page 2", "parent_id": self.category1.id}
        )
        page._onchange_parent_id()
        self.assertEqual(page.content, self.category1.template)

    def test_page_history_diff(self):
        page = self.page_obj.create(
            {"name": "Test Page 3", "content": "<p>Test content</p>"}
        )
        page.content = "New content"
        self.assertIsNotNone(page.history_ids[0].diff)

    def test_page_link(self):
        page = self.page_obj.create(
            {"name": "Test Page 3", "content": "<p>Test content</p>"}
        )
        self.assertEqual(
            page.backend_url,
            "/web#id={}&model=document.page&view_type=form".format(page.id),
        )
        menu = self.env.ref("knowledge.menu_document")
        page.menu_id = menu
        self.assertEqual(
            page.backend_url,
            "/web#id={}&model=document.page&view_type=form&action={}".format(
                page.id, menu.action.id
            ),
        )

    def test_open_folder_unreadable_parent(self):
        other_company = self.env["res.company"].create({"name": "Other company"})
        user = self.env["res.users"].create(
            {
                "name": "Page reader",
                "login": "page_reader",
                "groups_id": [
                    (6, 0, [self.env.ref("knowledge.group_document_user").id])
                ],
            }
        )
        hidden_root = self.page_obj.create(
            {
                "name": "Root folder of the other company",
                "type": "category",
                "company_id": other_company.id,
            }
        )
        hidden_folder = self.page_obj.create(
            {
                "name": "Folder of the other company",
                "type": "category",
                "parent_id": hidden_root.id,
                "company_id": other_company.id,
            }
        )
        shared_folder = self.page_obj.create(
            {
                "name": "Folder shared by all companies",
                "type": "category",
                "parent_id": hidden_folder.id,
                "company_id": False,
            }
        )
        self.page_obj.create(
            {
                "name": "Page of my company",
                "parent_id": shared_folder.id,
                "company_id": user.company_id.id,
                "content": "<p>Content</p>",
            }
        )
        self.page_obj.create(
            {
                "name": "Page of the other company",
                "parent_id": shared_folder.id,
                "company_id": other_company.id,
                "content": "<p>Content</p>",
            }
        )
        self.page_obj.flush()
        self.page_obj.invalidate_cache()
        with self.assertRaises(AccessError):
            hidden_folder.with_user(user).read(["name"])
        folder_form = common.Form(
            shared_folder.with_user(user), view="document_page.view_category_form"
        )
        self.assertIn("Page of my company", folder_form.content)
        self.assertNotIn("Page of the other company", folder_form.content)

    def test_page_copy(self):
        page = self.page_obj.create(
            {"name": "Test Page 3", "content": "<p>Test content</p>"}
        )
        page_copy = page.copy()
        self.assertEqual(page_copy.name, page.name + " (copy)")
        self.assertEqual(page_copy.content, page.content)
        self.assertEqual(page_copy.draft_name, "1.0")
        self.assertEqual(page_copy.draft_summary, "summary")
