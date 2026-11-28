from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    group_help_multilang = fields.Boolean(
        string="Multilingual Help",
        implied_group="screen_help.group_multilang",
        help="Help sections can be written for a given language.",
    )
