# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests import common


class TestDocumentUrl(common.TransactionCase):
    def setUp(self):
        super().setUp()
        wizard_add_url = self.env["ir.attachment.add_url"]

        self.wizard_add_url = wizard_add_url.with_context(
            active_model="res.users",
            active_id=self.env.ref("base.user_demo").id,
            active_ids=[self.env.ref("base.user_demo").id],
        ).create({"name": "Demo User (Website)", "url": "http://www.odoodemouser.com"})

    def test_add_url_attachment(self):
        self.wizard_add_url.action_add_url()
        domain = [
            ("type", "=", "url"),
            ("name", "=", "Demo User (Website)"),
            ("url", "=", "http://www.odoodemouser.com"),
            ("res_model", "=", "res.users"),
            ("res_id", "=", self.env.ref("base.user_demo").id),
        ]
        attachment_added_count = self.env["ir.attachment"].search_count(domain)
        self.assertEqual(attachment_added_count, 1)
        attachment = self.env["ir.attachment"].search(domain)
        self.assertEqual(attachment.mimetype, "application/link")
