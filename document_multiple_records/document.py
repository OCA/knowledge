# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2014 Savoir-faire Linux
#    (<http://www.savoirfairelinux.com>).
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

from openerp.osv import orm, fields


class document_file(orm.Model):
    _inherit = 'ir.attachment'

    _columns = {
        'attachment_document_ids': fields.one2many('ir.attachment.document',
                                                   'attachment_id',
                                                   'Records'),
    }

    def create(self, cr, uid, data, context=None):
        ir_attachment_document_obj = self.pool.get('ir.attachment.document')
        res = super(document_file, self).create(cr, uid, data, context=context)
        # Create attachment_document_ids with res_model, res_id and res_name
        if 'res_model' in data and 'res_id' in data:
            ir_attachment_document_obj.create(cr, uid, {
                'attachment_id': res,
                'res_model': data['res_model'],
                'res_id': data['res_id'],
                'res_name': data.get(
                    'res_name', self.pool.get(data['res_model']).browse(
                        cr, uid, data['res_id'],
                        context=context).name_get()[0][1]),
            }, context=context)
        return res

    def unlink(self, cr, uid, ids, context=None, check=True):
        ir_attach_doc_obj = self.pool.get('ir.attachment.document')
        if context is None:
            context = {}
        # Deleting from dropdown list in the form view
        res_model = context.get('multiple_records_res_model')
        res_id = context.get('multiple_records_res_id')
        if res_model and res_id:
            query = [
                ('res_model', '=', res_model),
                ('res_id', '=', res_id),
                ('attachment_id', 'in', ids),
            ]
            ids_to_unlink = ir_attach_doc_obj.search(
                cr, uid, query, context=context)
            result = ir_attach_doc_obj.unlink(
                cr, uid, ids_to_unlink, context=context)
        else:
            # Normal delete
            result = super(document_file, self).unlink(
                cr, uid, ids, context=context)
        return result


class ir_attachment_document(orm.Model):
    _description = 'Attachment Documents'
    _name = 'ir.attachment.document'

    _columns = {
        'res_id': fields.integer('Resource ID', readonly=True,
                                 help="The record id this is attached to."),
        'res_model': fields.char(
            'Resource Model', size=64, readonly=True,
            help="The database object this attachment will be attached to"),
        'res_name': fields.char('Resource Name', type='char',
                                size=128,
                                readonly=True),
        'attachment_id': fields.many2one(
            'ir.attachment', 'Attachment', ondelete='cascade'),
    }
