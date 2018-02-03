# -*- coding: utf-8 -*-
# © 2018 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from openerp import _, api, fields, models
from openerp.exceptions import AccessError, ValidationError


class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    lock_ids = fields.One2many(
        'ir.attachment.lock', 'attachment_id', 'Locks',
    )
    locked = fields.Boolean(compute='_compute_locked')
    can_lock = fields.Boolean(compute='_compute_locked')

    @api.multi
    @api.depends(
        'lock_ids.create_uid', 'lock_ids.shared_user_ids',
        'lock_ids.lock_type',
    )
    def _compute_locked(self):
        for this in self:
            this.locked = bool(this.lock_ids)
            this.can_lock = bool(
                this.mapped('lock_ids.create_uid') & this.env.user or
                'shared' in this.mapped('lock_ids.lock_type')
            ) or not this.locked and self.check_access_rights('write', False)

    @api.constrains('datas', 'datas_fname')
    def _constrain_datas(self):
        for this in self:
            if not this.lock_ids:
                continue
            if not this.can_lock:
                raise ValidationError(_('Attachment is locked'))

    @api.multi
    def lock(self, lock_type='exclusive', valid_until=None, data=None):
        data = data or {}
        if valid_until:
            data['valid_until'] = valid_until
        data['lock_type'] = lock_type
        for this in self:
            if not this.can_lock:
                raise AccessError(_('Unable to obtain lock'))
            if this.lock_ids:
                this.lock_ids.filtered(
                    lambda x: x.lock_type == lock_type
                ).sudo().write(dict(data, shared_user_ids=[(4, self.env.uid)]))
            else:
                this.write({'lock_ids': [(0, 0, data)]})

    @api.multi
    def unlock(self):
        return self.mapped('lock_ids').filtered(
            lambda x: x.create_uid & self.env.user or
            x.lock_type == 'shared' and x.shared_user_ids & self.env.user
        ).unlink()
