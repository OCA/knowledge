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
        'attachmentdocument_ids': fields.one2many('ir.attachment.document', 'attachment_id', 'Records'),
    }

    def unlink(self, cr, uid, ids, context=None, check=True):
        ir_attach_doc_obj = self.pool.get('ir.attachment.document')
        if context is None:
            context = {}
        for line in self.browse(cr, uid, ids, context=context):
            if line.attachmentdocument_ids:
                # Get the first document
                first_id = min(line.attachmentdocument_ids)

                result = self.write(cr, uid, ids, {'res_id': first_id.res_id,
                                                   'res_model': first_id.res_model,
                                                   'res_name': first_id.res_name, }, context=context)
                ir_attach_doc_obj.unlink(cr, uid, min(line.attachmentdocument_ids).id, context=context)
            else:
                result = super(document_file, self).unlink(cr, uid, ids, context=context)
        return result


class ir_attachment_document(orm.Model):
    _description = 'Attachment Documents'
    _name = 'ir.attachment.document'

    _columns = {
        'res_id': fields.integer('Resource ID', readonly=True,
                                 help="The record id this is attached to."),
        'res_model': fields.char('Resource Model', size=64,
                                 readonly=True,
                                 help="The database object this attachment will be attached to"),
        'res_name': fields.char('Resource Name', type='char',
                                size=128,
                                readonly=True),
        'attachment_id': fields.many2one('ir.attachment', 'Attachment'),
    }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
