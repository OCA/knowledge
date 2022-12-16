# Copyright 2022 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import base64

import odoo.tests


class TestAttachmentZippedDownload(odoo.tests.HttpCase):
    def setUp(self):
        super().setUp()
        test_1 = self._create_attachment("test1.txt")
        test_2 = self._create_attachment("test2.txt")
        self.attachments = test_1 + test_2
        self.user = self.env["res.users"].create(
            {
                "name": "test-user",
                "login": "test-user",
                "password": "test-user",
                "groups_id": [(6, 0, [self.env.ref("base.group_user").id])],
            }
        )

    def _create_attachment(self, name):
        return self.env["ir.attachment"].create(
            {
                "name": name,
                "datas": base64.b64encode(b"\xff data"),
            }
        )

    def test_action_attachments_download(self):
        self.authenticate("test-user", "test-user")
        # 16.0 WARNING odoo odoo.http: Sorry, you are not allowed to access this document.
        res = self.attachments.sudo().action_attachments_download()
        response = self.url_open(res["url"], timeout=20)
        self.assertEqual(response.status_code, 200)
