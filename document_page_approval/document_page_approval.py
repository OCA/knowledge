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
from openerp.osv import fields, orm
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT


class document_page_history_wkfl(orm.Model):
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
                    cr, uid, template_id, page.id, force_send=True
                )

        return True

    def page_approval_approved(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {
            'state': 'approved',
            'approved_date': datetime.now().strftime(
                DEFAULT_SERVER_DATETIME_FORMAT),
            'approved_uid': uid
        }, context=context)
        return True

    def can_user_approve_page(self, cr, uid, ids, name, args, context=None):
        user = self.pool.get('res.users').browse(cr, uid, uid, context=context)
        res = {}
        for page in self.browse(cr, uid, ids, context=context):
            res[page.id] = self.can_user_approve_this_page(page.page_id, user)

        return res

    def can_user_approve_this_page(self, page, user):
        if page:
            res = page.approver_gid in user.groups_id
            res = res or self.can_user_approve_this_page(page.parent_id, user)
        else:
            res = False

        return res

    def get_approvers_guids(self, cr, uid, ids, name, args, context=None):
        res = {}
        for page in self.browse(cr, uid, ids, context=context):
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

    def get_approvers_email(self, cr, uid, ids, name, args, context):
        res = {}
        for rec_id in ids:
            emails = ''
            guids = self.get_approvers_guids(
                cr, uid, ids, name, args, context=context)
            uids = self.pool.get('res.users').search(
                cr, uid, [('groups_id', 'in', guids[rec_id])])
            users = self.pool.get('res.users').browse(
                cr, uid, uids, context=context)

            for user in users:
                if user.email:
                    emails += user.email
                    emails += ','
                else:
                    empl_id = self.pool.get('hr.employee').search(
                        cr, uid, [('login', '=', user.login)])[0]
                    empl = self.pool.get('hr.employee').browse(
                        cr, uid, empl_id, context=context)
                    if empl.work_email:
                        emails += empl.work_email
                        emails += ','

            emails = emails[:-1]
            res[rec_id] = emails
        return res

    def get_page_url(self, cr, uid, ids, name, args, context):
        res = {}
        for rec_id in ids:
            base_url = self.pool.get('ir.config_parameter').get_param(
                cr, uid, 'web.base.url', default='http://localhost:8069',
                context=context)

            res[rec_id] = base_url + (
                '/#db=%s&id=%s&view_type=form&model=document.page.history' %
                (cr.dbname, rec_id))

        return res

    _columns = {
        'state': fields.selection([
            ('draft', 'Draft'),
            ('approved', 'Approved')], 'Status', readonly=True),
        'approved_date': fields.datetime("Approved Date"),
        'approved_uid': fields.many2one('res.users', "Approved By"),
        'is_parent_approval_required': fields.related(
            'page_id', 'is_parent_approval_required',
            string="parent approval", type='boolean', store=False),
        'can_user_approve_page': fields.function(
            can_user_approve_page, string="can user approve this page",
            type='boolean', store=False),
        'get_approvers_email': fields.function(
            get_approvers_email, string="get all approvers email",
            type='text', store=False),
        'get_page_url': fields.function(get_page_url, string="URL",
                                        type='text', store=False),
    }


class document_page_approval(orm.Model):
    _inherit = 'document.page'

    def _get_display_content(self, cr, uid, ids, name, args, context=None):
        res = {}
        for page in self.browse(cr, uid, ids, context=context):
            content = ""
            if page.type == "category":
                content = self._get_page_index(cr, uid, page, link=False)
            else:
                history = self.pool.get('document.page.history')
                if self.is_approval_required(page):
                    history_ids = history.search(
                        cr, uid, [
                            ('page_id', '=', page.id),
                            ('state', '=', 'approved')
                        ], limit=1, order='create_date DESC')
                    for h in history.browse(cr, uid, history_ids,
                                            context=context):
                        content = h.content
                else:
                    content = page.content
            res[page.id] = content
        return res

    def _get_approved_date(self, cr, uid, ids, name, args, context=None):
        res = {}
        for page in self.browse(cr, uid, ids, context=context):
            if self.is_approval_required(page):
                history = self.pool.get('document.page.history')
                history_ids = history.search(
                    cr, uid, [
                        ('page_id', '=', page.id),
                        ('state', '=', 'approved')
                    ], limit=1, order='create_date DESC')
                approved_date = False
                for h in history.browse(cr, uid, history_ids):
                    approved_date = h.approved_date
                res[page.id] = approved_date
            else:
                res[page.id] = ""

        return res

    def _get_approved_uid(self, cr, uid, ids, name, args, context=None):
        res = {}
        for page in self.browse(cr, uid, ids, context=context):
            if self.is_approval_required(page):
                history = self.pool.get('document.page.history')
                history_ids = history.search(cr, uid, [
                    ('page_id', '=', page.id),
                    ('state', '=', 'approved')], limit=1,
                    order='create_date DESC')
                approved_uid = False
                for h in history.browse(cr, uid, history_ids):
                    approved_uid = h.approved_uid.id
                res[page.id] = approved_uid
            else:
                res[page.id] = ""

        return res

    def _is_parent_approval_required(self, cr, uid, ids, name, args,
                                     context=None):
        res = {}
        for page in self.browse(cr, uid, ids, context=context):
            res[page.id] = self.is_approval_required(page)

        return res

    def is_approval_required(self, page):
        if page:
            res = page.approval_required
            res = res or self.is_approval_required(page.parent_id)
        else:
            res = False

        return res

    _columns = {
        'display_content': fields.function(
            _get_display_content, string='Displayed Content', type='text'),
        'approved_date': fields.function(
            _get_approved_date, string="Approved Date", type='datetime'),
        'approved_uid': fields.function(
            _get_approved_uid, string="Approved By", type='many2one',
            obj='res.users'),
        'approval_required': fields.boolean("Require approval"),
        'is_parent_approval_required': fields.function(
            _is_parent_approval_required, string="parent approval",
            type='boolean'),
        'approver_gid': fields.many2one("res.groups", "Approver group"),
    }
