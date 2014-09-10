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

    def get_attachment_extension(self, cr, uid, ids, context=None):
        result = {}
        for this in self.browse(
                cr, uid,
                ids if isinstance(ids, collections.Iterable) else [ids],
                context=context):
            if not this.id:
                result[this.id] = False
                continue
            extension = ''
            if this.datas_fname:
                filename, extension = os.path.splitext(this.datas_fname)
            if not extension:
                try:
                    import magic
                    ms = magic.open(magic.MAGIC_MIME_TYPE)
                    ms.load()
                    mimetype = ms.buffer(
                        base64.b64decode(this.datas))
                except ImportError:
                    (mimetype, encoding) = mimetypes.guess_type(
                        'data:;base64,' + this.datas, strict=False)
                extension = mimetypes.guess_extension(
                    mimetype, strict=False)

            result[this.id] = (extension or '').lstrip('.').lower()
        return result if isinstance(ids, collections.Iterable) else result[ids]
