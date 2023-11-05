# Copyright (C) 2023 Cetmix OÜ
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    is_active_google_api = fields.Boolean(
        string="Google APIs",
        config_parameter="document_url_google_drive.is_active_google_api",
    )
