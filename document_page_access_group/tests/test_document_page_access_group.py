# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.exceptions import UserError
from odoo.tests import common


class TestDocumentPageAccessGroup(common.TransactionCase):
    def setUp(self):
        super().setUp()
        self.document_user_group = self.browse_ref(
            "document_knowledge.group_document_user"
        ).id
        self.test_group = self.browse_ref("base.group_erp_manager").id
        self.user_id = self.env["res.users"].create(
            {
                "name": "user",
                "login": "user_login",
                "email": "user_email",
                "groups_id": [(4, self.document_user_group)],
            }
        )
        self.page = self.env["document.page"].create(
            {"name": "Page 1", "type": "content"}
        )

    def test_page_access(self):
        self.assertIsNone(self.page.with_user(self.user_id).check_access_rule("read"))
        self.page.write({"groups_id": [(4, self.test_group)]})
        with self.assertRaises(UserError):
            self.page.with_user(self.user_id).check_access_rule("read")
