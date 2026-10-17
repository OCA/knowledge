from . import controllers
from . import models


def post_init_hook(env):
    # help files of the modules installed before screen_help
    for module in env["ir.module.module"].search([("state", "=", "installed")]):
        env["help.section"]._load_markdown(module.name)
    # help of the actions left by help_popup, if any
    env["help.section"]._import_help_popup()
