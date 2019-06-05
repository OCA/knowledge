# -*- coding: utf-8 -*-
# © 2018 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from datetime import datetime, timedelta
from openerp import api, fields, models


class IrAttachmentLock(models.Model):
    _name = 'ir.attachment.lock'
    _description = 'Attachment lock'

    create_uid = fields.Many2one(
        'res.users', 'User', required=True, default=lambda self: self.env.user,
    )
    attachment_id = fields.Many2one(
        'ir.attachment', 'Attachment', required=True, index=True,
    )
    lock_type = fields.Selection(
        [('exclusive', 'Exclusive'), ('shared', 'Shared')],
        string='Type', required=True, default='shared',
    )
    application = fields.Selection(
        [('manual', 'Manual lock')], required=True, default='manual',
    )
    valid_until = fields.Datetime(
        required=True, default=fields.Datetime.to_string(
            datetime.now() + timedelta(hours=1),
        ),
    )
    shared_user_ids = fields.Many2many('res.users')

    _sql_constraints = [
        ('unique_attachment_id', 'unique(attachment_id)', 'Lock exists!'),
    ]

    @api.model
    def _cleanup_cron(self):
        self.search([
            ('valid_until', '<', fields.Datetime.to_string(datetime.now())),
        ]).unlink()
