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
from openerp import models, fields, api, _

_logger = logging.getLogger(__name__)


class document_page(models.Model):
    _name = "document.page"
    _inherit = ['mail.thread']
    _description = "Document Page"
    _order = 'name'

    name = fields.Char('Title', required=True)

    type = fields.Selection(
        [('content', 'Content'), ('category', 'Category')],
        'Type',
        help="Page type",
        default="content"
    )

    parent_id = fields.Many2one(
        'document.page',
        'Category',
        domain=[('type', '=', 'category')]
    )

    child_ids = fields.One2many(
        'document.page',
        'parent_id',
        'Children'
    )

    content = fields.Text(
        "Content"
    )

    display_content = fields.Text(
        string='Displayed Content',
        compute='_get_display_content'
    )

    history_ids = fields.One2many(
        'document.page.history',
        'page_id',
        'History'
    )

    menu_id = fields.Many2one(
        'ir.ui.menu',
        "Menu",
        readonly=True
    )

    create_date = fields.Datetime(
        "Created on",
        select=True,
        readonly=True
    )

    create_uid = fields.Many2one(
        'res.users',
        'Author',
        select=True,
        readonly=True
    )

    write_date = fields.Datetime(
        "Modification Date",
        select=True,
        readonly=True)

    write_uid = fields.Many2one(
        'res.users',
        "Last Contributor",
        select=True,
        readonly=True
    )

    def _get_page_index(self, page, link=True):
        index = []
        for subpage in page.child_ids:
            index += ["<li>" + self._get_page_index(subpage) +
                      "</li>"]
        r = ''
        if link:
            r = '<a href="#id=%s">%s</a>' % (page.id, page.name)

        if index:
            r += "<ul>" + "".join(index) + "</ul>"
        return r

    def _get_display_content(self):
        for page in self:
            if page.type == "category":
                display_content = self._get_page_index(page, link=False)
            else:
                display_content = page.content
            page.display_content = display_content

    @api.onchange("parent_id")
    def do_set_content(self):
        if self.parent_id and not self.content:
            if self.parent_id.type == "category":
                self.content = self.parent_id.content

    def create_history(self, page_id, content):
        history = self.env['document.page.history']
        return history.create({
            "content": content,
            "page_id": page_id
        })

    @api.multi
    def write(self, vals):
        result = super(document_page, self).write(vals)
        content = vals.get('content')
        if content:
            for page in self:
                self.create_history(page.id, content)
        return result

    @api.model
    @api.returns('self', lambda value: value.id)
    def create(self, vals):
        page_id = super(document_page, self).create(vals)
        content = vals.get('content')
        if content:
            self.create_history(page_id.id, content)
        return page_id


class document_page_history(models.Model):
    _name = "document.page.history"
    _description = "Document Page History"
    _order = 'id DESC'
    _rec_name = "create_date"

    page_id = fields.Many2one('document.page', 'Page')
    summary = fields.Char('Summary', size=256, select=True)
    content = fields.Text("Content")
    create_date = fields.Datetime("Date")
    create_uid = fields.Many2one('res.users', "Modified By")

    def getDiff(self, v1, v2):
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
