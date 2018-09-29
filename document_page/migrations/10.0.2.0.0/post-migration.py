# -*- coding: utf-8 -*-
# Copyright 2018 Ivan Todorovich <ivan.todorovich@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


def migrate(cr, version):  # pragma: no cover
    # Set all pre-existing categories template to its content
    cr.execute("""
        UPDATE document_page
        SET template = content
        WHERE type = 'category'
    """)
