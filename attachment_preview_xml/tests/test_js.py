# Copyright 2026 Jarsa
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import odoo.tests


@odoo.tests.tagged("post_install", "-at_install")
class TestXmlViewerJs(odoo.tests.HttpCase):
    def test_js(self):
        """Run the QUnit suite of this module in a real browser."""
        self.browser_js(
            "/web/tests?filter=attachment_preview_xml",
            "",
            "",
            login="admin",
            timeout=300,
        )
