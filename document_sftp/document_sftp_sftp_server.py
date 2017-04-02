# -*- coding: utf-8 -*-
# © 2016 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
try:
    from paramiko import SFTP_PERMISSION_DENIED, SFTPServerInterface,\
        SFTPServer
except ImportError:
    pass
from openerp import api


class DocumentSFTPSftpServerInterface(SFTPServerInterface):
    def __init__(self, server, env):
        self.env = env

    def list_folder(self, path):
        if not path or path in ('/', '.'):
            return self.env['document.sftp']._get_root_entries()
        handler = self.env['document.sftp']._get_handler_for(path)
        if handler is None:
            return SFTP_PERMISSION_DENIED
        return handler._list_folder(path)

    def lstat(self, path):
        if path == '.':
            return self.env['document.sftp.root']._directory('/')
        handler = self.env['document.sftp']._get_handler_for(path)
        if handler is None:
            return SFTP_PERMISSION_DENIED
        return handler._lstat(path)

    def stat(self, path):
        handler = self.env['document.sftp']._get_handler_for(path)
        if handler is None:
            return SFTP_PERMISSION_DENIED
        return handler._stat(path)

    def open(self, path, flags, attr):
        handler = self.env['document.sftp']._get_handler_for(path)
        if handler is None:
            return SFTP_PERMISSION_DENIED
        return handler._open(path, flags, attr)

    def session_ended(self):
        self.env.cr.close()
        return super(DocumentSFTPSftpServerInterface, self).session_ended()

    def session_started(self):
        self.env = self.env(cr=self.env.registry.cursor())


class DocumentSFTPSftpServer(SFTPServer):
    def start_subsystem(self, name, transport, channel):
        with api.Environment.manage():
            return super(DocumentSFTPSftpServer, self).start_subsystem(
                name, transport, channel)
