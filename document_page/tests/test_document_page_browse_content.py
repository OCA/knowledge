# Copyright 2026 NuoBiT Solutions SL - Eric Antones <eantones@nuobit.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo_test_helper import FakeModelLoader

from odoo.tests import common


class TestDocumentPageBrowseContent(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.loader = FakeModelLoader(cls.env, cls.__module__)
        cls.loader.backup_registry()
        cls.addClassCleanup(cls.loader.restore_registry)
        from .fake_models import DocumentPage

        cls.loader.update_registry((DocumentPage,))

    def test_folder_help(self):
        folder = self.env["document.page"].create(
            {"name": "Outer Folder", "type": "category"}
        )
        action = folder.action_view_children()
        self.assertEqual(action["help"], f"document.page {folder.id} [{folder.id}]")


@common.tagged("post_install", "-at_install")
class TestDocumentPageBrowseContentTour(common.HttpCase):
    def test_folder_card_breadcrumbs(self):
        common.new_test_user(
            self.env,
            login="reader_test",
            groups="document_knowledge.group_document_user",
            context={"no_reset_password": True},
            password="reader_test",
        )
        page_obj = self.env["document.page"]
        folder = page_obj.create({"name": "Outer Folder", "type": "category"})
        page_obj.create(
            {"name": "Inner Folder", "type": "category", "parent_id": folder.id}
        )
        page_obj.create({"name": "Other Folder", "type": "category"})
        self.start_tour(
            "/odoo/action-document_page.action_browse_top_content",
            "document_page_browse_content",
            login="reader_test",
        )
