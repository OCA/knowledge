# Copyright (C) 2023 Cetmix OÜ
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    is_active_google_api = fields.Boolean(
        string="Google APIs",
        config_parameter="is_active_google_api",
    )
    google_picker_client_id = fields.Char(
        string="Google Client ID",
        config_parameter="google_picker_client_id",
    )
    google_picker_api_key = fields.Char(
        string="Google API Key",
        config_parameter="google_picker_api_key",
    )
    google_picker_app_id = fields.Char(
        string="Google App ID",
        config_parameter="google_picker_app_id",
        default="odoo",
    )
