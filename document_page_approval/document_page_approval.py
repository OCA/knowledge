# -*- encoding: utf-8 -*-
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
from openerp import models, fields, SUPERUSER_ID


class document_page_history_wkfl(models.Model):
    _inherit = 'document.page.history'

    def page_approval_draft(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state': 'draft'})
        template_id = self.pool.get('ir.model.data').get_object_reference(
            cr, uid,
            'document_page_approval',
            'email_template_new_draft_need_approval')[1]
        for page in self.browse(cr, uid, ids, context=context):
            if page.is_parent_approval_required:
                self.pool.get('email.template').send_mail(
                    cr,
                    uid,
                    template_id,
                    page.id,
                    force_send=True
                )
        return True

    def page_approval_approved(self, cr, uid, ids, context=None):
        model_data_obj = self.pool.get('ir.model.data')
        message_obj = self.pool.get('mail.message')
        self.write(cr, uid, ids, {
            'state': 'approved',
            'approved_date': datetime.now().strftime(
                DEFAULT_SERVER_DATETIME_FORMAT),
            'approved_uid': uid
        }, context=context)
        # Notify followers a new version is available
        for page_history in self.browse(cr, uid, ids, context=context):
            subtype_id = model_data_obj.get_object_reference(
                cr, SUPERUSER_ID, 'mail', 'mt_comment')[1]
            message_obj.create(
                cr, uid,
                {'res_id': page_history.page_id.id,
                 'model': 'document.page',
                 'subtype_id': subtype_id,
                 'body': _('New version of the document %s'
                           ' approved.') % page_history.page_id.name
                 }
            )
        return True

    def _can_user_approve_page(self):
        user = self.env.user
        for page in self:
            page.can_user_approve_page = page.can_user_approve_this_page(
                page.page_id,
                user
            )

    def can_user_approve_this_page(self, page, user):
        if page:
            res = page.approver_gid in user.groups_id
            res = res or self.can_user_approve_this_page(page.parent_id, user)
        else:
            res = False
        return res

    def get_approvers_guids(self):
        res = {}
        for page in self:
            res[page.id] = self.get_approvers_guids_for_page(page.page_id)
        return res

    def get_approvers_guids_for_page(self, page):
        if page:
            if page.approver_gid:
                res = [page.approver_gid.id]
            else:
                res = []
            res.extend(self.get_approvers_guids_for_page(page.parent_id))
        else:
            res = []

        return res

    def _get_approvers_email(self):
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

    def _get_page_url(self):
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


class document_page_approval(models.Model):
    _inherit = 'document.page'

    def _get_display_content(self):
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

    def _get_approved_date(self):
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

    def _get_approved_uid(self):
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

    def _is_parent_approval_required(self):
        for page in self:
            page.is_parent_approval_required = self.is_approval_required(page)

    def is_approval_required(self, page):
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
