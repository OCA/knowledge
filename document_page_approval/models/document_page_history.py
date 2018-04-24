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

from openerp.tools.translate import _
from openerp import models, fields, api
from openerp.exceptions import UserError


class DocumentPageHistory(models.Model):
    """Useful to manage edition's workflow on a document."""

    _name = 'document.page.history'
    _inherit = ['document.page.history', 'mail.thread']

    state = fields.Selection([
        ('draft', 'Draft'),
        ('to approve', 'Pending Approval'),
        ('approved', 'Approved'),
        ('cancelled', 'Cancelled')],
        'Status',
        default='draft',
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
        related='page_id.am_i_approver',
        related_sudo=False,
    )

    page_url = fields.Text(
        compute='_compute_page_url',
        string="URL",
    )

    @api.multi
    def action_draft(self):
        """Set a change request as draft"""
        for rec in self:
            if not rec.state == 'cancelled':
                raise UserError(
                    _('You need to cancel it before reopening.'))
            if not (rec.am_i_owner or rec.am_i_approver):
                raise UserError(
                    _('You are not authorized to do this.\r\n'
                      'Only owners or approvers can reopen Change Requests.'))
            rec.write({'state': 'draft'})

    @api.multi
    def action_to_approve(self):
        """Set a change request as to approve"""
        template = self.env.ref(
            'document_page_approval.email_template_new_draft_need_approval')
        approver_gid = self.env.ref(
            'document_page_approval.group_document_approver_user')
        for rec in self:
            if rec.state != 'draft':
                raise UserError(
                    _("Can't approve pages in '%s' state.") % rec.state)
            if not (rec.am_i_owner or rec.am_i_approver):
                raise UserError(
                    _('You are not authorized to do this.\r\n'
                      'Only owners or approvers can request approval.'))
            # request approval
            if rec.is_approval_required:
                rec.write({'state': 'to approve'})
                guids = [g.id for g in rec.page_id.approver_group_ids]
                users = self.env['res.users'].search([
                    ('groups_id', 'in', guids),
                    ('groups_id', 'in', approver_gid.id)])
                rec.message_subscribe_users([u.id for u in users])
                rec.message_post_with_template(template.id)
            else:
                # auto-approve if approval is not required
                rec.action_approve()

    @api.multi
    def action_approve(self):
        """Set a change request as approved."""
        for rec in self:
            if rec.state not in ['draft', 'to approve']:
                raise UserError(
                    _("Can't approve page in '%s' state.") % rec.state)
            if not rec.am_i_approver:
                raise UserError(_(
                    'You are not authorized to do this.\r\n'
                    'Only approvers with these groups can approve this: '
                    ) % ', '.join(
                        [g.display_name
                            for g in rec.page_id.approver_group_ids]))
            # Update state
            rec.write({
                'state': 'approved',
                'approved_date': fields.datetime.now(),
                'approved_uid': self.env.uid,
            })
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
    def action_cancel(self):
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
    def action_cancel_and_draft(self):
        """Set a change request as draft, cancelling it first"""
        self.action_cancel()
        self.action_draft()

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
