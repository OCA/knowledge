# Copyright 2024 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    """Pages that had roles should now have the correct users."""
    pages = env["document.page"].sudo().search([("role_ids", "!=", False)])
    for page in pages:
        users = page.mapped("role_ids.users")
        page.role_ids = False
        page.user_ids = users
