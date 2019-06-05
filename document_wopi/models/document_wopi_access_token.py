# -*- coding: utf-8 -*-
# © 2017 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import time
import mimetypes
import os.path
import uuid
import urllib
import urlparse
from datetime import datetime, timedelta
from openerp import api, fields, models
from openerp.exceptions import AccessDenied


class DocumentWopiAccessToken(models.Model):
    _name = 'document.wopi.access.token'
    _description = 'Access token for WOPI requests'

    user_id = fields.Many2one(
        'res.users', 'User', required=True, ondelete='cascade',
    )
    attachment_id = fields.Many2one(
        'ir.attachment', 'Attachment', required=True, ondelete='cascade',
    )
    valid_until = fields.Datetime()
    token = fields.Char(required=True)
    token_ttl = fields.Integer(compute='_compute_token_ttl')
    action_url = fields.Char(compute='_compute_action_url')

    @api.model
    def _get_token(self, attachment):
        """Create or return a token ID for some attachment for the current
        user. This implies creating a shared lock for the attachment"""
        result = self.search([
            ('user_id', '=', self.env.user.id),
            ('attachment_id', '=', attachment.id),
            '|',
            ('valid_until', '=', False),
            ('valid_until', '>=', fields.Datetime.now()),
        ], limit=1)
        valid_until = fields.Datetime.to_string(
            datetime.now() +
            timedelta(self.env['ir.config_parameter'].get_param(
                'document_wopi.token_validity', 1800,
            ))
        )
        if result:
            result.write({'valid_until': valid_until})
        else:
            result = self.create({
                'user_id': self.env.user.id,
                'attachment_id': attachment.id,
                'valid_until': valid_until,
                # TODO: is this random enough or do we need some secret
                # generator?
                'token': str(uuid.uuid4()),
            })
        result.attachment_id.lock(lock_type='shared', valid_until=valid_until)
        return result

    @api.multi
    def _compute_token_ttl(self):
        for this in self:
            if not this.valid_until:
                continue
            this.token_ttl = int(time.mktime(
                fields.Datetime.from_string(this.valid_until).timetuple()
            ))

    @api.multi
    def _compute_action_url(self):
        wopi = self.env['document.wopi']
        discovery = wopi._discovery()
        for this in self:
            dummy, ext = os.path.splitext(this.attachment_id.datas_fname)
            if not ext:
                ext = mimetypes.guess_extension(this.attachment_id.file_type)
            if not ext:
                continue
            ext = ext[1:]
            action = discovery.get(
                (ext, 'edit'), discovery.get((ext, 'view')),
            )
            if not action:
                continue

            this.action_url = wopi._get_url(
                action.get('urlsrc', '')
            ) + '?' + urllib.urlencode({
                'WOPISrc': urlparse.urljoin(
                    self.env['ir.config_parameter']
                    .get_param('web.base.url'),
                    '/wopi/files/%d' % this.attachment_id.id,
                )
            })

    @api.model
    def _verify_token(self, token):
        """Be sure a token is valid; return a falsy value for invalid tokens"""
        access_token = self.search([('token', '=', token)])
        if not access_token:
            return self.browse([])
        try:
            access_token.attachment_id.sudo(access_token.user_id).read([])
        except AccessDenied:
            return self.browse([])
        if access_token.valid_until < fields.Datetime.now():
            return self.browse([])
        return access_token.sudo(access_token.user_id)
