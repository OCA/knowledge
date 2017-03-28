# -*- coding: utf-8 -*-
# © 2016 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from paramiko import SFTP_EOF, SFTP_OK, SFTP_PERMISSION_DENIED, SFTPHandle
from base64 import b64decode, b64encode
from openerp.models import NewId
from openerp.exceptions import AccessError


class DocumentSFTPHandle(SFTPHandle):
    def __init__(self, record, flags=0):
        self.record = record
        super(DocumentSFTPHandle, self).__init__(flags)

    def stat(self):
        return self.record.env['document.sftp.root']._file(self.record)

    def read(self, offset, length):
        data = b64decode(self.record.datas)
        if offset > len(data):
            return SFTP_EOF
        return data[offset:offset + length]

    def write(self, offset, write_data):
        data = b64decode(self.record.datas) if self.record.datas else ''
        if offset > len(data):
            return SFTP_EOF
        try:
            self.record.update({
                'datas': b64encode(
                    data[0:offset] + write_data +
                    data[offset + len(write_data):]
                ),
            })
            if isinstance(self.record.id, NewId):
                self.record.create(self.record._cache)
        except AccessError:
            return SFTP_PERMISSION_DENIED

        # we need this commit, because this runs in its own thread with its own
        # cursor
        self.record.env.cr.commit()
        # TODO: do we want to clear caches here?
        return SFTP_OK
