# -*- coding: utf-8 -*-
# Copyright 2018 Ivan Todorovich <ivan.todorovich@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


def migrate(cr, version):  # pragma: no cover
    # Set all pre-existing pages history to approved
    cr.execute("""
        UPDATE document_page_history
        SET state='approved',
            approved_uid=create_uid,
            approved_date=create_date
        WHERE state IS NULL
    """)
