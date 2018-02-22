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

from openerp import models, fields, api
from ast import literal_eval


class DocumentPageApproval(models.Model):
    """Useful to know the state of a document."""

    _inherit = 'document.page'

    history_ids = fields.One2many(
        order='approved_date DESC',
        domain=[('state', '=', 'approved')],
    )

    approved_date = fields.Datetime(
        compute='_compute_approved_info',
        string="Approved Date"
    )

    approved_uid = fields.Many2one(
        'res.users',
        compute='_compute_approved_info',
        string="Approved By",
    )

    approval_required = fields.Boolean(
        'Require approval',
        help='Require approval for changes on this page or its child pages.',
    )

    approver_gid = fields.Many2one(
        "res.groups",
        "Approver group",
        help='Users must also belong to the Approvers group',
    )

    is_approval_required = fields.Boolean(
        'Approval required',
        help='If true, changes of this page require approval',
        compute='_compute_is_approval_required',
    )

    approver_group_ids = fields.Many2many(
        'res.groups',
        string='Approver groups',
        help='Groups that can approve changes to this document',
        compute='_compute_approver_group_ids',
    )

    has_changes_pending_approval = fields.Boolean(
        compute='_compute_has_changes_pending_approval',
        string='Has changes pending approval'
    )

    @api.multi
    @api.depends('history_ids')
    def _compute_approved_info(self):
        """Return the approved date of a document."""
        for page in self:
            if page.history_ids:
                page.approved_date = page.history_ids[0].approved_date
                page.approved_uid = page.history_ids[0].approved_uid

    @api.multi
    @api.depends('approval_required', 'parent_id.is_approval_required')
    def _compute_is_approval_required(self):
        """Check if the document required approval based on his parents."""
        for page in self:
            res = page.approval_required
            if page.parent_id:
                res = res or page.parent_id.is_approval_required
            page.is_approval_required = res

    @api.multi
    @api.depends('approver_gid', 'parent_id.approver_group_ids')
    def _compute_approver_group_ids(self):
        """Compute the approver groups based on his parents."""
        for page in self:
            res = page.approver_gid
            if page.parent_id:
                res = res | page.parent_id.approver_group_ids
            page.approver_group_ids = res

    @api.multi
    def _compute_has_changes_pending_approval(self):
        history = self.env['document.page.history']
        for rec in self:
            changes = history.search_count([
                ('page_id', '=', rec.id),
                ('state', '=', 'to approve')])
            rec.has_changes_pending_approval = (changes > 0)

    @api.multi
    def _create_history(self, vals):
        res = super(DocumentPageApproval, self)._create_history(vals)
        res.signal_workflow('document_page_auto_confirm')

    @api.multi
    def action_changes_pending_approval(self):
        self.ensure_one()
        action = self.env.ref('document_page_approval.action_change_requests')
        action = action.read()[0]
        context = literal_eval(action['context'])
        context['search_default_page_id'] = self.id
        context['default_page_id'] = self.id
        action['context'] = context
        return action
