# Copyright 2026 GMI Fabrica
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    """Clear duplicate references before adding the DB unique constraint.

    The oldest record of each duplicated reference keeps its value; the rest
    are left without a reference.
    """
    openupgrade.logged_query(
        env.cr,
        """
        WITH duplicates AS (
            SELECT id,
                   ROW_NUMBER() OVER (
                       PARTITION BY reference ORDER BY id
                   ) AS rn
            FROM document_page
            WHERE reference IS NOT NULL
        )
        UPDATE document_page dp
        SET reference = NULL
        WHERE id IN (SELECT id FROM duplicates WHERE rn > 1)
        """,
    )
