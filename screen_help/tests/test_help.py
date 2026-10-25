from unittest.mock import patch

from odoo import Command as cmd
from odoo.exceptions import UserError
from odoo.tests import HttpCase, TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestHelp(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env["res.lang"]._activate_lang("fr_FR")
        cls.Section = cls.env["help.section"]
        cls.action = cls.env.ref("base.action_partner_form")
        # demo data
        cls.Section.search([]).unlink()

    def _content(self, lang):
        return self.action.with_context(lang=lang)._help_html()[0]

    def test_markdown(self):
        self.Section._load_markdown("screen_help", "demo_help")
        sections = self.action.help_section_ids
        self.assertEqual(len(sections), 2)
        self.assertEqual(set(sections.mapped("module")), {"screen_help"})
        self.assertIn("<table>", self._content("en_US"))
        self.assertNotIn("SIRET", self._content("en_US"))
        self.assertIn("SIRET", self._content("fr_FR"))
        # a section of a file can't be edited in Odoo, only reordered
        section = sections.filtered(lambda s: not s.lang)
        self.assertEqual(section.file, "demo_help/base.action_partner_form.md")
        with self.assertRaises(UserError):
            section.content = "<p>Edited</p>"
        section.sequence = 5
        # reloaded when the file changes
        section.checksum = "changed"
        self.Section._load_markdown("screen_help", "demo_help")
        self.assertIn("<table>", section.content)

    def test_help_popup(self):
        # columns left by help_popup in the database
        self.env.cr.execute(
            "ALTER TABLE ir_act_window ADD COLUMN IF NOT EXISTS enduser_help text, "
            "ADD COLUMN IF NOT EXISTS advanced_help text"
        )
        self.env.cr.execute(
            "UPDATE ir_act_window SET enduser_help = '<p>For users</p>', "
            "advanced_help = 'For developers' WHERE id = %s",
            [self.action.id],
        )
        sections = self.Section._import_help_popup()
        self.assertEqual(sections.action_id, self.action)
        self.assertIn("For users", sections[0].content)
        self.assertIn("Advanced Help", sections[1].content)
        self.assertIn("For developers", sections[1].content)
        # not imported twice
        self.assertFalse(self.Section._import_help_popup())

    def test_front_matter(self):
        header, text = self.Section._front_matter("---\nsequence: 20\n---\n## Title\n")
        self.assertEqual(header, {"sequence": "20"})
        self.assertEqual(text, "## Title\n")
        self.assertEqual(self.Section._front_matter("## Title\n"), ({}, "## Title\n"))

    def test_menu(self):
        menu = self.env["ir.ui.menu"].create(
            {
                "name": "Help Root",
                "child_id": [
                    cmd.create(
                        {
                            "name": "Partners",
                            "action": f"{self.action._name},{self.action.id}",
                        }
                    ),
                ],
            }
        )
        self.assertFalse(menu._help_actions())
        self.Section.create({"action_id": self.action.id, "content": "<p>Hi</p>"})
        self.assertEqual(menu._help_actions(), self.action)
        html = self.env["ir.ui.view"]._render_template(
            "screen_help.app_help_page", {"menu": menu}
        )
        self.assertIn("Hi", html)
        # sidebar: the action, then its headings
        self.assertEqual(
            menu._help_html()[1], [(1, f"help_{self.action.id}", self.action.name)]
        )
        # a section of the model is shown on its actions, and alone
        model = self.env["ir.model"]._get("res.partner")
        self.Section.create({"model_id": model.id, "content": "<h2>Model</h2>"})
        self.assertIn("Model", self.action._help_html()[0])
        self.assertTrue(self.Section.get_help(False, "res.partner")["has_help"])
        # application help: the model help is shown once, whatever its actions
        action2 = self.action.copy()
        menu.child_id[0].copy({"action": f"{action2._name},{action2.id}"})
        helps = menu._help_html()[0]
        self.assertEqual([a for a, __ in helps], [self.action])


@tagged("post_install", "-at_install")
class TestPopup(HttpCase):
    def test_window(self):
        action = self.env.ref("base.action_partner_form")
        self.env["help.section"].search([]).unlink()  # demo data
        self.env["help.section"].create(
            {"action_id": action.id, "content": "<h2>Usage</h2><p>Hi</p>"}
        )
        menu = self.env.ref("base.menu_administration")
        self.authenticate("admin", "admin")
        res = self.url_open(f"/screen_help?action_id={action.id}&menu_id={menu.id}")
        self.assertEqual(res.status_code, 200)
        self.assertIn("<p>Hi</p>", res.text)
        # table of contents
        self.assertIn(f'<h2 id="help_{action.id}_0">Usage</h2>', res.text)
        self.assertIn(f'href="#help_{action.id}_0"', res.text)
        self.assertIn(f"/screen_help/app/{menu.id}", res.text)
        self.assertEqual(res.text.count("<!DOCTYPE html>"), 1)
        self.assertIn("data:image/", res.text)  # company logo
        self.assertIn("screen_help_edit", res.text)  # edit button (admin)
        # screen without action: help of the model only
        model = self.env["ir.model"]._get("res.partner")
        self.env["help.section"].create(
            {"model_id": model.id, "content": "<p>Model</p>"}
        )
        res = self.url_open("/screen_help?model=res.partner")
        self.assertIn("<p>Model</p>", res.text)
        self.assertNotIn("<p>Hi</p>", res.text)
        self.assertNotIn("#1f2228", res.text)
        # dark color scheme (web_enterprise: preference of the user)
        IrHttp = type(self.env["ir.http"])
        with patch.object(IrHttp, "color_scheme", lambda self: "dark", create=True):
            res = self.url_open(f"/screen_help/app/{menu.id}")
        self.assertIn("#1f2228", res.text)
