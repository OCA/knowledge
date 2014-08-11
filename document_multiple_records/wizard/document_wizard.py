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

from openerp.osv import fields, orm
from openerp.tools.translate import _


class document_wizard(orm.Model):
    _name = "ir.attachment.existing.doc"
    _description = "Add existing document/attachment wizard"
    _columns = {
        'attachment_ids': fields.many2many('ir.attachment',
                                           'document_attachment_rel',
                                           'wizard_id',
                                           'attachment_id',
                                           'Attachments'),
    }

    def action_apply(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        ir_attach_obj = self.pool.get('ir.attachment')
        ir_attach_doc_obj = self.pool.get('ir.attachment.document')
        ir_model_obj = self.pool.get(
            context.get('model') or context.get('active_model'))

        name = ir_model_obj.browse(
            cr, uid, context.get('ids') or context.get('active_ids'),
            context=context)[0]['name']
        data = self.read(cr, uid, ids, [], context=context)[0]
        if not data['attachment_ids']:
            raise orm.except_orm(
                _('Error'),
                _('You have to select at least 1 Document. And try again'))
        for attach in ir_attach_obj.browse(cr, uid, data['attachment_ids'],
                                           context=context):
            data_attach = {
                'res_model': context.get('model') or
                context.get('active_model'),
                'res_id': context.get('ids') and context.get('ids')[0] or
                context.get('active_id'),
                'res_name': name,
                'attachment_id': attach.id,
            }
            # Created attachment_document_ids
            ir_attach_doc_obj.create(cr, uid, data_attach, context=context)
        return {'type': 'ir.actions.act_window_close'}
