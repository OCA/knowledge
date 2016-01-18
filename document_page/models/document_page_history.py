# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
import logging
import difflib
from openerp import models, fields, _

_logger = logging.getLogger(__name__)


class DocumentPageHistory(models.Model):
    """This model is necessary to manage a document history."""

    _name = "document.page.history"
    _description = "Document Page History"
    _order = 'id DESC'
    _rec_name = "create_date"

    page_id = fields.Many2one('document.page', 'Page')
    summary = fields.Char('Summary', select=True)
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
