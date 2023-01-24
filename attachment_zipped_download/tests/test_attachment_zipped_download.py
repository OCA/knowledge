# Copyright 2022-2023 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import base64

import odoo.tests
from odoo.tests import new_test_user


class TestAttachmentZippedDownload(odoo.tests.HttpCase):
    def setUp(self):
        super().setUp()
        ctx = {
            "mail_create_nolog": True,
            "mail_create_nosubscribe": True,
            "mail_notrack": True,
            "no_reset_password": True,
        }
        self.user = new_test_user(
            self.env,
            login="test-user",
            context=ctx,
        )
        test_1 = self._create_attachment(self.user, "test1.txt")
        test_2 = self._create_attachment(self.user, "test2.txt")
        self.attachments = test_1 + test_2

    def _create_attachment(self, user, name):
        return (
            self.env["ir.attachment"]
            .with_user(user)
            .create(
                {
                    "name": name,
                    "datas": base64.b64encode(b"\xff data"),
                }
            )
        )

    def test_action_attachments_download(self):
        self.authenticate("test-user", "test-user")
        res = self.attachments.action_attachments_download()
        response = self.url_open(res["url"], timeout=20)
        self.assertEqual(response.status_code, 200)
