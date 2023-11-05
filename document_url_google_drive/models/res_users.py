# Copyright (C) 2023 Cetmix OÜ
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResUsers(models.Model):
    _inherit = "res.users"
    google_picker_client_id = fields.Char(string="Google Client ID")
    google_picker_api_key = fields.Char(string="Google API Key")
    google_picker_scope = fields.Char(
        string="Google Scope",
        default="https://www.googleapis.com/auth/drive.readonly",
    )
    google_picker_app_id = fields.Char(
        string="Google App ID",
        default="odoo",
    )
    google_picker_access_token = fields.Char(string="Google Access Token")
    google_picker_mime_types = fields.Char(string="Google Mime Types")

    def get_google_picker_params(self):
        """
        Get Google Picker params
        :return: dict
        """
        self.ensure_one()
        is_active_google_api = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("document_url_google_drive.is_active_google_api")
        )
        if not is_active_google_api:
            return {}
        return {
            "client_id": self.google_picker_client_id,
            "api_key": self.google_picker_api_key,
            "scope": self.google_picker_scope,
            "app_id": self.google_picker_app_id,
            "access_token": self.google_picker_access_token,
            "mime_types": self.google_picker_mime_types,
        }

    def save_google_picker_access_token(self, access_token):
        """
        Save Google Picker access token
        :param access_token: str
        :return: None
        """
        self.ensure_one()
        self.google_picker_access_token = access_token
