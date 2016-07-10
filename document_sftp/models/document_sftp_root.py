# -*- coding: utf-8 -*-
# © 2016 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import stat
try:
    from paramiko import SFTPAttributes
    from ..document_sftp_handle import DocumentSFTPHandle
except ImportError:   # pragma: no cover
    pass
from openerp import api, models


class DocumentSFTPRoot(models.AbstractModel):
    _name = 'document.sftp.root'
    _description = 'Base class for virtual roots in SFTP'

    @api.model
    def _directory(self, name):
        """Return SFTPAttributes for a directory with given name"""
        result = SFTPAttributes()
        result.filename = name
        result.st_uid = 0
        result.st_group = 0
        result.st_size = 0
        result.st_mode = stat.S_IFDIR | stat.S_IRUSR | stat.S_IXUSR
        return result

    @api.model
    def _file(self, attachment):
        """Return SFTPAttributes for a given attachment"""
        if not hasattr(attachment, '_ids'):
            attachment = self.env['ir.attachment'].browse(attachment)
        result = SFTPAttributes()
        result.filename = attachment.datas_fname or attachment.name
        result.st_uid = 0
        result.st_group = 0
        result.st_size = attachment.file_size
        result.st_mode = stat.S_IFREG | stat.S_IRUSR
        return result

    @api.model
    def _file_handle(self, attachment):
        """Return a DocumentSFTPHandle for a given attachment"""
        return DocumentSFTPHandle(attachment)

    @api.model
    def _get_root_attributes(self):
        """Return the entry in the root folder as SFTPAttributes"""
        raise NotImplementedError()

    @api.model
    def _stat(self, path):
        """Return file attributes"""
        raise NotImplementedError()

    @api.model
    def _open(self, path, flags, attr):
        """Return file attributes"""
        raise NotImplementedError()

    @api.model
    def _lstat(self, path):
        """Return attributes about a link"""
        return self._stat(path)
