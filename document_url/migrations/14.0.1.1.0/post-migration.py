# Copyright 2021 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE ir_attachment
        SET mimetype = 'text/css'
        WHERE mimetype = 'application/link' AND res_id = 0 AND name LIKE '%.%css'
        """,
    )
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE ir_attachment
        SET mimetype = 'application/javascript'
        WHERE mimetype = 'application/link' AND res_id = 0 AND name LIKE '%.js'
        """,
    )
