# -*- coding: utf-8 -*-
# © 2017 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import base64
import json
import time
import logging
from openerp import http, fields
from openerp.http import request
_logger = logging.getLogger(__name__)


class WopiEndpoints(http.Controller):
    @http.route(
        '/wopi/files/<model("ir.attachment"):attachment>', type='http',
        auth='public',
    )
    def files(self, attachment, access_token, **kwargs):
        token = self._verify(access_token)
        if not token:
            _logger.error(request.httprequest.headers)
            return request.not_found()
        attachment = token.attachment_id
        _logger.debug(request.httprequest.headers)
        return json.dumps({
            'BaseFileName': attachment.name,
            'OwnerId': attachment.create_uid.id,
            'Size': attachment.file_size,
            'UserId': token.user_id.id,
            'Version': str(self._timestamp(attachment)),
            'UserFriendlyName': token.user_id.display_name,
            'UserCanWrite': attachment.check_access_rights('write', False),
            'SupportsUpdate': True,
            'SupportsGetLock': True,
            'SupportsLocks': True,
            'LastModifiedTime': fields.Datetime.from_string(
                attachment.write_date
            ).isoformat(),
            'UserCanNotWriteRelative': True,
            'DisablePrint': False,
            'DisableExport': False,
            'DisableCopy': False,
            'DisableInactiveMessages': False,
            'HidePrintOption': False,
            'HideSaveOption': False,
            'HideExportOption': False,
            'EnableOwnerTermination': False,
            'UserExtraInfo': False,
            'WatermarkText': '',
            'PostMessageOrigin': False,
        })

    @http.route(
        '/wopi/files/<model("ir.attachment"):attachment>/contents',
        type='http', auth='public',
    )
    def files_contents(self, attachment, access_token, **kwargs):
        token = self._verify(access_token)
        attachment = token.attachment_id
        if not token:
            _logger.error(request.httprequest.headers)
            return request.not_found()
        _logger.debug(request.httprequest.headers)
        if 'X-WOPI-Override' in request.httprequest.headers:
            name = '_files_contents_%s' % (
                request.httprequest.headers['X-WOPI-Override']
            )
            if hasattr(self, name):
                return getattr(self, name)(attachment, token, **kwargs)
            return request.not_found()
        return request.make_response(
            base64.b64decode(attachment.datas),
            [('X-WOPI-ItemVersion', str(self._timestamp(attachment)))],
        )

    def _files_contents_PUT(self, attachment, token, **kwargs):
        if not attachment.can_lock:
            return request.not_found()
        if not attachment.locked:
            attachment.lock()
        attachment.write({'datas': base64.b64encode(request.httprequest.data)})
        return request.make_response(
            json.dumps({
                'LastModifiedTime': fields.Datetime.from_string(
                    attachment.create_date
                ).isoformat(),
            }),
            [
                ('X-WOPI-Lock', str(attachment.lock_ids.ids)),
                ('X-WOPI-ItemVersion', str(self._timestamp(attachment))),
            ],
        )

    def _verify(self, access_token):
        return request.env['document.wopi.access.token'].sudo()._verify_token(
            access_token
        )

    def _timestamp(self, attachment):
        return int(time.mktime(
            fields.Datetime.from_string(attachment.write_date).timetuple()
        ))
