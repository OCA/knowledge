# Copyright (C) 2023 Cetmix OÜ
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo.tests import common


class TestDocumentUrl(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.wizard_add_url = cls.env["ir.attachment.add_url"]
        cls.config_settings = cls.env["ir.config_parameter"].sudo()
        cls.users = cls.env["res.users"]

    def test_add_google_drive_url_attachment(self):
        self.wizard_add_url.add_attachment_google_drive(
            "http://www.odoodemouser.com",
            "Demo User (Website)",
            "res.users",
            [self.env.ref("base.user_demo").id],
        )
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

    def test_get_google_picker_params_is_active(self):
        self.config_settings.set_param("is_active_google_api", True)
        self.config_settings.set_param("google_picker_api_key", "test_api_key")
        self.config_settings.set_param("google_picker_app_id", "test_app_id")
        self.config_settings.set_param("google_picker_client_id", "test_client_id")
        user = self.users.with_context(no_reset_password=True).create(
            {
                "name": "Test User",
                "login": "test_user",
                "google_picker_scope": "test_scope",
                "google_picker_access_token": "test_access_token",
                "google_picker_mime_types": "test_mime_types",
                "google_picker_expires_date": 0,
            }
        )
        params = user.get_google_picker_params()
        self.assertEqual(
            params,
            {
                "client_id": "test_client_id",
                "api_key": "test_api_key",
                "scope": "test_scope",
                "app_id": "test_app_id",
                "access_token": "test_access_token",
                "expires_date": 0,
                "mime_types": "test_mime_types",
            },
        )

    def test_get_google_picker_params_not_is_active(self):
        self.config_settings.set_param("is_active_google_api", False)
        user = self.users.with_context(no_reset_password=True).create(
            {
                "name": "Test User",
                "login": "test_user",
            }
        )
        params = user.get_google_picker_params()
        self.assertEqual(
            params,
            {},
        )
