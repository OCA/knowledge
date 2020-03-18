# -*- coding: utf-8 -*-
# Copyright (C) 2013 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class DocumentPageApproval(models.Model):
    """Useful to know the state of a document."""

    _inherit = 'document.page'

    @api.multi
    def _get_display_content(self):
        """Display the content of document."""
        for page in self:
            content = ""
            if page.type == "category":
                content = self._get_page_index(page, link=False)
            else:
                history = self.env['document.page.history']
                if self.is_approval_required(page):
                    history_ids = history.search(
                        [
                            ('page_id', '=', page.id),
                            ('state', '=', 'approved')
                        ],
                        limit=1,
                        order='create_date DESC'
                    )
                    content = history_ids.content
                else:
                    content = page.content
            page.display_content = content

    @api.multi
    def _get_approved_date(self):
        """Return the approved date of a document."""
        for page in self:
            approved_date = False
            if self.is_approval_required(page):
                history = self.env['document.page.history']
                history_ids = history.search(
                    [
                        ('page_id', '=', page.id),
                        ('state', '=', 'approved')
                    ],
                    limit=1,
                    order='create_date DESC'
                )
                approved_date = history_ids.approved_date
            page.approved_date = approved_date

    @api.multi
    def _get_approved_uid(self):
        """Return the user's id of the approved user."""
        for page in self:
            approved_uid = False
            if self.is_approval_required(page):
                history = self.env['document.page.history']
                history_ids = history.search(
                    [
                        ('page_id', '=', page.id),
                        ('state', '=', 'approved')
                    ],
                    limit=1,
                    order='create_date DESC'
                )
                approved_uid = history_ids.approved_uid.id
            page.approved_uid = approved_uid

    @api.multi
    def _is_parent_approval_required(self):
        """Check if the document requires approval base on his parent."""
        for page in self:
            page.is_parent_approval_required = self.is_approval_required(page)

    def is_approval_required(self, page):
        """Check if a document requires approval."""
        if page:
            res = page.approval_required
            res = res or self.is_approval_required(page.parent_id)
        else:
            res = False
        return res

    display_content = fields.Text(
        compute=_get_display_content,
        string='Displayed Content'
    )

    approved_date = fields.Datetime(
        compute=_get_approved_date,
        string="Approved Date"
    )

    approved_uid = fields.Many2one(
        'res.users',
        compute=_get_approved_uid,
        string="Approved By",
    )

    approval_required = fields.Boolean("Require approval")

    is_parent_approval_required = fields.Boolean(
        compute=_is_parent_approval_required,
        string="parent approval"
    )

    approver_gid = fields.Many2one(
        "res.groups",
        "Approver group"
    )
