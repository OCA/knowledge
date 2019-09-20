# Copyright 2019 Tecnativa - Jairo Llopis
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

def migrate(cr, version):
    """Stored URLs need to define a filename."""
    cr.execute("""
        UPDATE ir_attachment
        SET filename = name
        WHERE filename IS NULL AND type = 'url'
    """)
