# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2013 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
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

from datetime import datetime
from openerp.tools.translate import _
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT
from openerp import models, fields, api


class DocumentPageHistoryWorkflow(models.Model):
    """Useful to manage edition's workflow on a document."""

    _inherit = 'document.page.history'

    @api.multi
    def page_approval_draft(self):
        """Set a document state as draft and notified the reviewers."""
        self.write({'state': 'draft'})
        template = self.env.ref(
            'document_page_approval.email_template_new_draft_need_approval')
        for page in self:
            if page.is_parent_approval_required:
                template.send_mail(page.id, force_send=True)
        return True

    @api.multi
    def page_approval_approved(self):
        """Set a document state as approve."""
        message_obj = self.env['mail.message']
        self.write({
            'state': 'approved',
            'approved_date': datetime.now().strftime(
                DEFAULT_SERVER_DATETIME_FORMAT),
            'approved_uid': self.env.uid
        })
        # Notify followers a new version is available
        for page_history in self:
            subtype = self.env.ref('mail.mt_comment')
            message_obj.create(
                {'res_id': page_history.page_id.id,
                 'model': 'document.page',
                 'subtype_id': subtype.id,
                 'body': _('New version of the document %s'
                           ' approved.') % page_history.page_id.name
                 }
            )
        return True

    @api.multi
    def _can_user_approve_page(self):
        """Check if a user cas approve the page."""
        user = self.env.user
        for page in self:
            page.can_user_approve_page = page.can_user_approve_this_page(
                page.page_id,
                user
            )

    def can_user_approve_this_page(self, page, user):
        """Check if a user can approved the page."""
        if page:
            res = page.approver_gid in user.groups_id
            res = res or self.can_user_approve_this_page(page.parent_id, user)
        else:
            res = False
        return res

    @api.multi
    def get_approvers_guids(self):
        """Return the approvers group."""
        res = {}
        for page in self:
            res[page.id] = self.get_approvers_guids_for_page(page.page_id)
        return res

    def get_approvers_guids_for_page(self, page):
        """Return the approvers group for a page."""
        if page:
            if page.approver_gid:
                res = [page.approver_gid.id]
            else:
                res = []
            res.extend(self.get_approvers_guids_for_page(page.parent_id))
        else:
            res = []

        return res

    @api.multi
    def _get_approvers_email(self):
        """Get the approvers email."""
        for page in self:
            emails = ''
            guids = self.get_approvers_guids()
            uids = [i.id for i in self.env['res.users'].search([
                ('groups_id', 'in', guids[page.id])
            ])]
            users = self.env['res.users'].browse(uids)

            for user in users:
                if user.email:
                    emails += user.email
                    emails += ','
                else:
                    empl = self.env['hr.employee'].search([
                        ('login', '=', user.login)
                    ])
                    if empl.work_email:
                        emails += empl.work_email
                        emails += ','

            page.get_approvers_email = emails[:-1]

    @api.multi
    def _get_page_url(self):
        """Get the page url."""
        for page in self:
            base_url = self.env['ir.config_parameter'].get_param(
                'web.base.url',
                default='http://localhost:8069'
            )

            page.get_page_url = (
                '{}/web#db={}&id={}&view_type=form&'
                'model=document.page.history').format(
                    base_url,
                    self.env.cr.dbname,
                    page.id
                )

    state = fields.Selection(
        [('draft', 'Draft'), ('approved', 'Approved')],
        'Status',
        readonly=True
    )

    approved_date = fields.Datetime("Approved Date")

    approved_uid = fields.Many2one(
        'res.users',
        "Approved By"
    )

    is_parent_approval_required = fields.Boolean(
        related='page_id.is_parent_approval_required',
        string="parent approval",
        store=False
    )

    can_user_approve_page = fields.Boolean(
        compute=_can_user_approve_page,
        string="can user approve this page",
        store=False
    )
    get_approvers_email = fields.Text(
        compute=_get_approvers_email,
        string="get all approvers email",
        store=False
    )
    get_page_url = fields.Text(
        compute=_get_page_url,
        string="URL",
        store=False
    )
