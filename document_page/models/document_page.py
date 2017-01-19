# -*- coding: utf-8 -*-
# Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class DocumentPage(models.Model):
    """This class is use to manage Document."""

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

    content = fields.Text("Content")

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
        readonly=True
    )

    create_uid = fields.Many2one(
        'res.users',
        'Author',
        readonly=True
    )

    write_date = fields.Datetime(
        "Modification Date",
        readonly=True
    )

    write_uid = fields.Many2one(
        'res.users',
        "Last Contributor",
        readonly=True
    )

    def _get_page_index(self, page, link=True):
        """Return the index of a document."""
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
        """Return the content of a document."""
        for page in self:
            if page.type == "category":
                display_content = self._get_page_index(page, link=False)
            else:
                display_content = page.content
            page.display_content = display_content

    @api.onchange("parent_id")
    def do_set_content(self):
        """We Set it the right content to the new parent."""
        if self.parent_id and not self.content:
            if self.parent_id.type == "category":
                self.content = self.parent_id.content

    def create_history(self, page_id, content):
        """Create the first history of a newly created document."""
        history = self.env['document.page.history']
        return history.create({
            "content": content,
            "page_id": page_id
        })

    @api.multi
    def write(self, vals):
        """Write the content and set the history."""
        result = super(DocumentPage, self).write(vals)
        content = vals.get('content')
        if content:
            for page in self:
                self.create_history(page.id, content)
        return result

    @api.model
    @api.returns('self', lambda value: value.id)
    def create(self, vals):
        """Create the first history of a document."""
        page_id = super(DocumentPage, self).create(vals)
        content = vals.get('content')
        if content:
            self.create_history(page_id.id, content)
        return page_id
