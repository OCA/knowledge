# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2014 Therp BV (<http://therp.nl>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
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
import collections
import os.path
import mimetypes
import base64
from openerp.osv.orm import Model


class IrAttachment(Model):
    _inherit = 'ir.attachment'

    def get_binary_extension(
            self, cr, uid, model, ids, binary_field, filename_field=None,
            context=None):
        result = {}
        for this in self.pool[model].browse(
                cr, uid,
                ids if isinstance(ids, collections.Iterable) else [ids],
                context=context):
            if not this.id:
                result[this.id] = False
                continue
            extension = ''
            if filename_field and this[filename_field]:
                filename, extension = os.path.splitext(this[filename_field])
            if not this[binary_field]:
                result[this.id] = False
                continue
            if not extension:
                try:
                    import magic
                    ms = magic.open(
                        hasattr(magic, 'MAGIC_MIME_TYPE') and
                        magic.MAGIC_MIME_TYPE or magic.MAGIC_MIME)
                    ms.load()
                    mimetype = ms.buffer(
                        base64.b64decode(this[binary_field]))
                except ImportError:
                    (mimetype, encoding) = mimetypes.guess_type(
                        'data:;base64,' + this[binary_field], strict=False)
                extension = mimetypes.guess_extension(
                    mimetype.split(';')[0], strict=False)

            result[this.id] = (extension or '').lstrip('.').lower()
        return result if isinstance(ids, collections.Iterable) else result[ids]

    def get_attachment_extension(self, cr, uid, ids, context=None):
        return self.get_binary_extension(
            cr, uid, self._name, ids, 'datas', 'datas_fname', context=context)
