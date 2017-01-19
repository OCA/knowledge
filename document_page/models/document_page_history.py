# -*- coding: utf-8 -*-
# Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
import difflib
from odoo import fields, models
from odoo.tools.translate import _

_logger = logging.getLogger(__name__)


class DocumentPageHistory(models.Model):
    """This model is necessary to manage a document history."""

    _name = "document.page.history"
    _description = "Document Page History"
    _order = 'id DESC'
    _rec_name = "create_date"

    page_id = fields.Many2one('document.page', 'Page')
    summary = fields.Char('Summary', index=True)
    content = fields.Text("Content")
    create_date = fields.Datetime("Date")
    create_uid = fields.Many2one('res.users', "Modified By")

    def getDiff(self, v1, v2):
        """Return the difference between two version of document version."""
        text1 = self.browse(v1).content
        text2 = self.browse(v2).content
        line1 = line2 = ''
        if text1:
            line1 = text1.splitlines(1)
        if text2:
            line2 = text2.splitlines(1)
        if (not line1 and not line2) or (line1 == line2):
            return _('There are no changes in revisions.')
        else:
            diff = difflib.HtmlDiff()
            return diff.make_table(
                line1, line2,
                "Revision-{}".format(v1),
                "Revision-{}".format(v2),
                context=True
            )
