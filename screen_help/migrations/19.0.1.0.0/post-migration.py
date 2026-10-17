from odoo import SUPERUSER_ID, api


def migrate(cr, version):
    # update from help_popup renamed to screen_help (e.g. by OpenUpgrade)
    env = api.Environment(cr, SUPERUSER_ID, {})
    env["help.section"]._import_help_popup()
