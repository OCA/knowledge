# Copyright 2019 Creu Blanca
# Copyright 2025 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from markupsafe import Markup

from odoo.addons.base.tests.common import BaseCommon


class TestDocumentReferenceLink(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.page_obj = cls.env["document.page"]
        cls.history_obj = cls.env["document.page.history"]
        cls.page1 = cls.page_obj.create(
            {"name": "Test Page 1", "content": Markup("{{r2}}"), "reference": "R1"}
        )
        cls.page2 = cls.page_obj.create(
            {"name": "Test Page 2", "content": Markup("{{r1}}"), "reference": "r2"}
        )

    def test_check_raw(self):
        self.assertEqual(
            str(self.page2.display_name), str(self.page1.get_raw_content())
        )

    def test_get_formview_action(self):
        res = self.page1.get_formview_action()
        view_id = self.env.ref("document_page.view_wiki_form").id
        expected_keys = {
            "type": "ir.actions.act_window",
            "res_model": "document.page",
            "res_id": self.page1.id,
            "target": "current",
            "views": [(view_id, "form")],
        }
        for key, expected_value in expected_keys.items():
            self.assertEqual(res.get(key), expected_value, f"Mismatch in key: {key}")

    def test_compute_content_parsed(self):
        self.page1.content = Markup("<p>{{r2}}</p>")
        self.assertIn("data-oe-model='document.page'", self.page1.content_parsed)
        self.assertIn(f"data-oe-id='{self.page2.id}'", self.page1.content_parsed)
        self.assertIn(f"href='{self.page2.backend_url}'", self.page1.content_parsed)
        self.assertIn("Test Page 2", self.page1.content_parsed)

    def test_inverse_content_replacement(self):
        self.page1.content = "{{r2}}"
        self.assertIn(f"data-oe-id='{self.page2.id}'", self.page1.content)
        self.assertIn(f"href='{self.page2.backend_url}'", self.page1.content_parsed)
        self.assertNotIn("&lt;a", self.page1.content)
