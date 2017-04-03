# -*- coding: utf-8 -*-
# © 2016 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
try:
    from paramiko import SFTP_EOF, SFTPHandle
except ImportError:
    pass
from base64 import b64decode


class DocumentSFTPHandle(SFTPHandle):
    def __init__(self, attachment, flags=0):
        self.attachment = attachment
        super(DocumentSFTPHandle, self).__init__(flags)

    def stat(self):
        return self.attachment.env['document.sftp.root']._file(self.attachment)

    def read(self, offset, length):
        # pylint: disable=W8106
        data = b64decode(self.attachment.datas)
        if offset > len(data):
            return SFTP_EOF
        return data[offset:offset + length]
