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
import base64
import collections
import logging
import mimetypes
import os.path

from openerp.osv.orm import Model

_logger = logging.getLogger(__name__)


class IrAttachment(Model):
    _inherit = 'ir.attachment'

    def get_binary_extension(
            self, cr, uid, model, ids, binary_field, filename_field=None,
            context=None):
        result = {}
        context_bin_size = dict(context or {})
        context_bin_size['bin_size'] = True
        ids_to_browse = ids if isinstance(ids, collections.Iterable) \
            else [ids]
        # First pass: load fields in bin_size mode to avoid loading big files
        #  unnecessarily.
        if filename_field:
            for this in self.pool[model].browse(cr, uid, ids_to_browse,
                                                context=context_bin_size):
                if not this.id:
                    result[this.id] = False
                    continue
                extension = ''
                if this[filename_field]:
                    filename, extension = os.path.splitext(
                        this[filename_field])
                if this[binary_field] and extension:
                    result[this.id] = extension
                    _logger.debug('Got extension %s from filename %s',
                                  extension, this[filename_field])
        # Second pass for all attachments which have to be loaded fully
        #  to get the extension from the content
        ids_to_browse = [_id for _id in ids_to_browse if _id not in result]
        for this in self.pool[model].browse(cr, uid, ids_to_browse,
                                            context=context):
            if this[binary_field] is None:
                result[this.id] = False
                continue
            try:
                import magic
                ms = magic.open(
                    hasattr(magic, 'MAGIC_MIME_TYPE') and
                    magic.MAGIC_MIME_TYPE or magic.MAGIC_MIME)
                ms.load()
                if model == self._name and binary_field == 'datas'\
                        and this.store_fname:
                    mimetype = ms.file(
                        this._full_path(this.store_fname))
                    _logger.debug('Magic determined mimetype %s from file %s',
                                  mimetype, this.store_fname)
                else:
                    mimetype = ms.buffer(
                        base64.b64decode(this[binary_field]))
                    _logger.debug('Magic determined mimetype %s from buffer',
                                  mimetype)
            except ImportError:
                (mimetype, encoding) = mimetypes.guess_type(
                    'data:;base64,' + this[binary_field], strict=False)
                _logger.debug('Mimetypes guessed type %s from buffer',
                              mimetype)
            extension = mimetypes.guess_extension(
                mimetype.split(';')[0], strict=False)
            result[this.id] = extension
        for _id in result:
            result[_id] = (result[_id] or '').lstrip('.').lower()
        return result if isinstance(ids, collections.Iterable) else result[ids]

    def get_attachment_extension(self, cr, uid, ids, context=None):
        return self.get_binary_extension(
            cr, uid, self._name, ids, 'datas', 'datas_fname', context=context)
