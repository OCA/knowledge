# -*- coding: utf-8 -*-
# Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import exceptions, fields, models
from odoo.tools.translate import _


class DocumentPageShowDiff(models.TransientModel):
    """Display Difference for History."""

    _name = 'wizard.document.page.history.show_diff'

    def get_diff(self):
        """Return the Difference between two document."""
        history = self.env["document.page.history"]
        ids = self.env.context.get('active_ids', [])

        diff = ""
        if len(ids) == 2:
            if ids[0] > ids[1]:
                diff = history.getDiff(ids[1], ids[0])
            else:
                diff = history.getDiff(ids[0], ids[1])
        elif len(ids) == 1:
            old = history.browse(ids[0])
            nids = history.search(
                [('page_id', '=', old.page_id.id)],
                order='id DESC',
                limit=1
            )
            diff = history.getDiff(ids[0], nids.id)
        else:
            raise exceptions.Warning(
                _("Select one or maximum two history revisions!")
            )
        return diff

    diff = fields.Text(
        'Diff',
        readonly=True,
        default=get_diff
    )
