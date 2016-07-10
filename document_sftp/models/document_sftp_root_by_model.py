# -*- coding: utf-8 -*-
# © 2016 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import os
from openerp import api, models
try:
    from paramiko import SFTP_NO_SUCH_FILE, SFTP_PERMISSION_DENIED
except ImportError:   # pragma: no cover
    pass


class DocumentSFTPRootByModel(models.Model):
    _inherit = 'document.sftp.root'
    _name = 'document.sftp.root.by_model'
    _virtual_root = 'By model'
    _virtual_root_by_id = 'By id'

    @api.model
    def _get_root_attributes(self):
        return self._directory(self._virtual_root)

    @api.model
    def _stat(self, path):
        path = path.strip('/')
        if not path.startswith(self._virtual_root):
            return SFTP_NO_SUCH_FILE
        components = path.split('/')
        if len(components) == 1:
            return self._get_root_attributes()
        elif len(components) in (2, 3):
            return self._directory(components[-1])
        elif len(components) == 4:
            return self._file(self.env['ir.attachment'].search([
                ('res_model', '=', components[-3]),
                ('res_id', '=', components[-2]),
                '|',
                ('datas_fname', '=', components[-1]),
                ('name', '=', components[-1]),
            ], limit=1))
        return SFTP_NO_SUCH_FILE

    @api.model
    def _list_folder(self, path):
        path = path.strip('/')
        components = path.split('/')
        result = []
        if len(components) == 1:
            for model in self.env['ir.model'].search([
                ('osv_memory', '=', False),
            ]):
                if not self.env['ir.model.access'].check(
                    model.model, raise_exception=False
                ):
                    continue
                result.append(self._directory(model.model))
        elif len(components) == 2:
            model = components[-1]
            seen = set([])
            if model not in self.env.registry:
                return SFTP_NO_SUCH_FILE
            for attachment in self.env['ir.attachment'].search([
                ('res_model', '=', model),
                ('res_id', '!=', False),
            ], order='res_id asc'):
                # TODO: better lump ids together in steps of 100 or something?
                if attachment.res_id not in seen:
                    seen.add(attachment.res_id)
                    result.append(self._directory(str(attachment.res_id)))
        elif len(components) == 3:
            model = components[-2]
            res_id = int(components[-1])
            for attachment in self.env['ir.attachment'].search([
                ('res_model', '=', model),
                ('res_id', '=', res_id),
            ]):
                result.append(self._file(attachment))
        else:
            return SFTP_NO_SUCH_FILE
        return result

    @api.model
    def _open(self, path, flags, attr):
        if flags & os.O_WRONLY or flags & os.O_RDWR:
            # TODO: do something more sensible here
            return SFTP_PERMISSION_DENIED
        path = path.strip('/')
        components = path.split('/')
        if len(components) == 4:
            return self._file_handle(self.env['ir.attachment'].search([
                ('res_model', '=', components[-3]),
                ('res_id', '=', components[-2]),
                '|',
                ('datas_fname', '=', components[-1]),
                ('name', '=', components[-1]),
            ], limit=1))
        return SFTP_PERMISSION_DENIED
