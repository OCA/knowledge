# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2015 Therp BV (<http://therp.nl>).
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
import logging
from openerp.osv import orm, fields
from base64 import b64decode


class Attachment(orm.Model):
    _inherit = 'ir.attachment'

    def update_file_type_from_cron(self, cr, uid, count=1000, context=None):
        ids = self.search(
            cr, uid, [('file_type', '=', False)], context=context)
        logging.getLogger('openerp.addons.attachment_file_type').info(
            'Found %s attachments without file type in the database.',
            len(ids))
        self.update_file_type(cr, uid, ids, force=True, context=None)

    def update_file_type(self, cr, uid, ids, force=False, context=None):
        """ Write the file types for these attachments. If the document module
        is installed, don't do anything unless in force mode. """
        if not ids:
            return True
        if not force:
            cr.execute(
                "SELECT id from ir_module_module WHERE name = 'document' "
                "AND state = 'installed'")
            if cr.fetchone():
                return True
        if isinstance(ids, (int, long)):
            ids = [ids]

        logger = logging.getLogger('openerp.addons.attachment_file_type')
        import magic
        ms = magic.open(
            # MAGIC_MIME gives additional encoding, but old versions of the
            # 'file' package come with py_magic.c that lack MAGIC_MIME_TYPE
            magic.MAGIC_MIME_TYPE if hasattr(magic, 'MAGIC_MIME_TYPE')
            else magic.MAGIC_MIME)
        ms.load()
        for attachment_id in ids:
            attachment = self.browse(cr, uid, attachment_id, context=context)
            file_type = ms.buffer(
                b64decode(attachment.datas)).split(';')[0]
            logger.debug(
                'Found file type %s for attachment with id %s',
                file_type, attachment.id)
            attachment.write({'file_type': file_type})
        return True

    def write(self, cr, uid, ids, vals, context=None):
        """ Update the mime type when the contents are overwritten """
        res = super(Attachment, self).write(
            cr, uid, ids, vals, context=context)
        if vals.get('datas'):
            self.update_file_type(cr, uid, ids, context=context)
        return res

    def create(self, cr, uid, vals, context=None):
        """ Determine the mime type when the attachment is created """
        res_id = super(Attachment, self).create(
            cr, uid, vals, context=context)
        if vals.get('datas'):
            self.update_file_type(cr, uid, [res_id], context=context)
        return res_id

    _columns = {
        'file_type': fields.char('Content Type', size=128),
        }
