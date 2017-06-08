# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Agile Business Group sagl
#    (<http://www.agilebg.com>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
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

from openerp.osv import orm, fields
import os.path
import threading


class IrAttachment(orm.Model):
    _inherit = 'ir.attachment'

    def __init__(self, *args, **kwargs):
        self._file_extension_lock = threading.RLock()
        self._extension = None
        super(IrAttachment, self).__init__(*args, **kwargs)

    def _full_path(self, cr, uid, path):
        # every calls to this method is managed using by _file_extension_lock
        # to avoid the risk of overwriting the _extension attribute
        full_path = super(IrAttachment, self)._full_path(cr, uid, path)
        if self._extension:
            full_path += self._extension
        return full_path

    def _data_set(self, cr, uid, id, name, value, arg, context=None):
        with self._file_extension_lock:
            attachment = self.browse(cr, uid, id, context=context)
            if attachment.datas_fname:
                filename, extension = os.path.splitext(attachment.datas_fname)
                self._extension = extension
                attachment.write({'extension': extension})
            super(IrAttachment, self)._data_set(
                cr, uid, id, name, value, arg, context=context)

    def _data_get(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for attachment in self.browse(cr, uid, ids, context=context):
            if attachment.extension:
                with self._file_extension_lock:
                    self._extension = attachment.extension
                    res.update(
                        super(IrAttachment, self)._data_get(
                            cr, uid, [attachment.id], name, arg,
                            context=context))
            else:
                res.update(
                    super(IrAttachment, self)._data_get(
                        cr, uid, [attachment.id], name, arg,
                        context=context))
        return res

    def unlink(self, cr, uid, ids, context=None):
        for attachment in self.browse(cr, uid, ids, context=context):
            if attachment.extension:
                with self._file_extension_lock:
                    self._extension = attachment.extension
                    super(IrAttachment, self).unlink(
                        cr, uid, ids, context=context)
            else:
                super(IrAttachment, self).unlink(cr, uid, ids, context=context)

    _columns = {
        'datas': fields.function(
            _data_get, fnct_inv=_data_set, string='File Content',
            type="binary", nodrop=True),
        'extension': fields.char(string='Attachment File Extension', size=4),
    }
