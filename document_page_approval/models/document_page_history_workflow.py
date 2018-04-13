# -*- coding: utf-8 -*-
# Copyright (C) 2013 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime
from odoo.tools.translate import _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo import api, fields, models


class DocumentPageHistoryWorkflow(models.Model):
    """Useful to manage edition's workflow on a document."""

    _name = 'document.page.history'
    _inherit = ['document.page.history', 'mail.thread']

    state = fields.Selection([
        ('draft', 'Draft'),
        ('to approve', 'Pending Approval'),
        ('approved', 'Approved'),
        ('cancelled', 'Cancelled')],
        'Status',
        readonly=True,
    )

    approved_date = fields.Datetime(
        'Approved Date',
    )

    approved_uid = fields.Many2one(
        'res.users',
        'Approved by',
    )

    is_approval_required = fields.Boolean(
        related='page_id.is_approval_required',
        string="Approval required",
    )

    am_i_owner = fields.Boolean(
        compute='_compute_am_i_owner'
    )

    am_i_approver = fields.Boolean(
        related='page_id.am_i_approver'
    )

    page_url = fields.Text(
        compute='_compute_page_url',
        string="URL",
    )

    @api.multi
    def page_approval_draft(self):
        """Set a change request as draft"""
        self.write({'state': 'draft'})

    @api.multi
    def page_approval_to_approve(self):
        """Set a change request as to approve"""
        self.write({'state': 'to approve'})
        template = self.env.ref(
            'document_page_approval.email_template_new_draft_need_approval')
        approver_gid = self.env.ref(
            'document_page_approval.group_document_approver_user')
        for rec in self:
            if rec.is_approval_required:
                guids = [g.id for g in rec.page_id.approver_group_ids]
                users = self.env['res.users'].search([
                    ('groups_id', 'in', guids),
                    ('groups_id', 'in', approver_gid.id)])
                rec.message_subscribe_users([u.id for u in users])
                rec.message_post_with_template(template.id)

    @api.multi
    def page_approval_approved(self):
        """Set a change request as approved."""
        self.write({
            'state': 'approved',
            'approved_date': datetime.now().strftime(
                DEFAULT_SERVER_DATETIME_FORMAT),
            'approved_uid': self.env.uid
        })
        for rec in self:
            # Trigger computed field update
            rec.page_id._compute_history_head()
            # Notify state change
            rec.message_post(
                subtype='mt_comment',
                body=_(
                    'Change request has been approved by %s.'
                    ) % (self.env.user.name)
            )
            # Notify followers a new version is available
            rec.page_id.message_post(
                subtype='mt_comment',
                body=_(
                    'New version of the document %s approved.'
                    ) % (rec.page_id.name)
            )

    @api.multi
    def page_approval_cancelled(self):
        """Set a change request as cancelled."""
        self.write({'state': 'cancelled'})
        for rec in self:
            rec.message_post(
                subtype='mt_comment',
                body=_(
                    'Change request <b>%s</b> has been cancelled by %s.'
                    ) % (rec.display_name, self.env.user.name)
                )

    @api.multi
    def _compute_am_i_owner(self):
        """Check if current user is the owner"""
        for rec in self:
            rec.am_i_owner = (rec.create_uid == self.env.user)

    @api.multi
    def _compute_page_url(self):
        """Compute the page url."""
        for page in self:
            base_url = self.env['ir.config_parameter'].get_param(
                'web.base.url',
                default='http://localhost:8069'
            )

            page.page_url = (
                '{}/web#db={}&id={}&view_type=form&'
                'model=document.page.history').format(
                    base_url,
                    self.env.cr.dbname,
                    page.id
                )

    @api.multi
    def _compute_diff(self):
        """Shows a diff between this version and the previous version"""
        history = self.env['document.page.history']
        for rec in self:
            domain = [
                ('page_id', '=', rec.page_id.id),
                ('state', '=', 'approved')]
            if rec.approved_date:
                domain.append(('approved_date', '<', rec.approved_date))
            prev = history.search(domain, limit=1, order='approved_date DESC')
            if prev:
                rec.diff = self.getDiff(prev.id, rec.id)
            else:
                rec.diff = self.getDiff(False, rec.id)
