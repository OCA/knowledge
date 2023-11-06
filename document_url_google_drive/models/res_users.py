# Copyright (C) 2023 Cetmix OÜ
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResUsers(models.Model):
    _inherit = "res.users"

    google_picker_scope = fields.Char(
        string="Google Scope",
        default="https://www.googleapis.com/auth/drive.readonly",
    )
    google_picker_access_token = fields.Char(string="Google Access Token")
    google_picker_expires_date = fields.Integer(string="Google Expires Date")
    google_picker_mime_types = fields.Char(string="Google Mime Types")
    google_picker_active = fields.Boolean(
        compute="_compute_google_picker_active",
    )

    def get_google_picker_params(self):
        """
        Get Google Picker params
        :return: dict
        """
        self.ensure_one()
        config = self.env["ir.config_parameter"].sudo()
        google_service = self.env["google.service"]

        if not self.google_picker_active:
            return {}
        return {
            "client_id": google_service._get_client_id("picker"),
            "api_key": config.get_param("google_picker_api_key"),
            "app_id": config.get_param("google_picker_app_id"),
            "scope": self.google_picker_scope,
            "access_token": self.google_picker_access_token,
            "expires_date": self.google_picker_expires_date,
            "mime_types": self.google_picker_mime_types,
        }

    def save_google_picker_access_token(self, access_token, expires_date):
        """
        Save Google Picker access token
        :param access_token: str
        :return: None
        """
        self.ensure_one()
        self.google_picker_access_token = access_token
        self.google_picker_expires_date = expires_date

    def _compute_google_picker_active(self):
        """
        Compute Google Picker Active
        :return: None
        """
        conf = self.env["ir.config_parameter"].sudo()
        self.google_picker_active = conf.get_param("is_active_google_api")
