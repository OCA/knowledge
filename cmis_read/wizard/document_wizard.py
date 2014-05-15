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
from openerp.tools.translate import _
from openerp.addons.connector.session import ConnectorSession
from openerp.addons.connector.queue.job import job
import logging
_logger = logging.getLogger(__name__)


class ir_attachment_dms(orm.TransientModel):
    _name = 'ir.attachment.dms'

    _columns = {
        'name': fields.char('File name', size=150,
                            readonly=True,
                            help="File name"),
        'owner': fields.char('Owner', size=150,
                             readonly=True,
                             help="Owner"),
        'file_id': fields.char('File ID', size=150,
                               readonly=True,
                               help="File Id"),
    }


class ir_attachment_edm_wizard(orm.Model):
    _name = 'ir.attachment.dms.wizard'

    _columns = {
        'name': fields.char('File name', size=150, help="File name"),
        'attachment_ids': fields.many2many('ir.attachment.dms',
                                           'document_attachment_dms_rel',
                                           'wizard_id', 'attachment_id',
                                           'Attachments'),
    }

    # Search documents from dms.
    def search_doc(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        this = self.browse(cr, uid, ids, context=context)[0]
        data = self.read(cr, uid, ids, [], context=context)[0]
        if not data['name']:
            raise orm.except_orm(_('Error'),
                                 _('You have to fill in the file name.' +
                                   'And try again'))
        if not hasattr(ids, '__iter__'):
            ids = [ids]
        session = ConnectorSession(cr, uid, context=context)
        file_name = data['name']
        for backend_id in ids:
            search_doc_from_dms(session, 'ir.attachment',
                                backend_id, file_name)
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'ir.attachment.dms.wizard',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': this.id,
            'views': [(False, 'form')],
            'target': 'new',
        }

    # Adding documents from Document Management (EDM) to OE.
    def action_apply(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        model = context['model']
        res_id = context['ids'][0]
        ir_model_obj = self.pool.get(context['model'])
        name = ir_model_obj.browse(cr, uid, context['ids'],
                                   context=context)[0]['name']
        data = self.read(cr, uid, ids, [], context=context)[0]
        if not data['attachment_ids']:
            raise orm.except_orm(_('Error'),
                                 _('You have to select at least 1 Document.' +
                                   'And try again'))
        if not hasattr(ids, '__iter__'):
            ids = [ids]
        session = ConnectorSession(cr, uid, context=context)
        for backend_id in ids:
            # Create doc in OE from DMS.
            create_doc_from_dms.delay(session, 'ir.attachment', backend_id,
                                      data, name, model, res_id, uid)
        return {'type': 'ir.actions.act_window_close'}


def search_doc_from_dms(session, model_name, backend_id, file_name):
    ir_attach_dms_obj = session.pool.get('ir.attachment.dms')
    cmis_backend_obj = session.pool.get('cmis.backend')
    if session.context is None:
        session.context = {}
    # login with the cmis account
    repo = cmis_backend_obj._auth(session.cr, session.uid,
                                  context=session.context)

    # Search name of doc and delete it if the document is already existed
    attachment_ids = ir_attach_dms_obj.search(session.cr, session.uid, [])
    ir_attach_dms_obj.unlink(session.cr, session.uid,
                             attachment_ids, context=session.context)
    # Escape the name for characters not supported in filenames
    # for avoiding SQL Injection
    file_name = file_name.replace("'", "\\'")
    file_name = file_name.replace("%", "\%")
    file_name = file_name.replace("_", "\_")
    # Get results from name of document
    results = repo.query(" SELECT cmis:name, cmis:createdBy, cmis:objectId, "
                         "cmis:contentStreamLength FROM  cmis:document "
                         "WHERE cmis:name LIKE '%" + file_name + "%'")
    for result in results:
        info = result.getProperties()
        if info['cmis:contentStreamLength'] != 0:
            data_attach = {
                'name': info['cmis:name'],
                'owner': info['cmis:createdBy'],
                'file_id': info['cmis:objectId'],
            }
        ir_attach_dms_obj.create(session.cr, session.uid, data_attach,
                                 context=session.context)


@job
def create_doc_from_dms(session, model_name, backend_id, data, name,
                        model, res_id, uid, filters=None):
    ir_attach_obj = session.pool.get('ir.attachment')
    ir_attach_dms_obj = session.pool.get('ir.attachment.dms')
    cmis_backend_obj = session.pool.get('cmis.backend')
    if session.context is None:
        session.context = {}
    # login with the cmis account
    repo = cmis_backend_obj._auth(
        session.cr, session.uid, context=session.context)
    for attach in ir_attach_dms_obj.browse(session.cr, session.uid,
                                           data['attachment_ids'],
                                           context=session.context):
        # Get results from id of document
        results = repo.query(" SELECT * FROM  cmis:document WHERE \
                             cmis:objectId ='" + attach.file_id + "'")
        for result in results:
            info = result.getProperties()
            data_attach = {
                'name': info['cmis:name'],
                'description': info['cmis:description'],
                'type': 'binary',
                'datas': result.getContentStream().read().encode('base64'),
                'res_model': model,
                'res_name': name,
                'res_id': res_id,
                'user_id': uid,
            }
            session.context['bool_read_doc'] = True
            ir_attach_obj.create(session.cr, session.uid,
                                 data_attach, context=session.context)
    return True

# vim:expandtab:smartindent:toabstop=4:softtabstop=4:shiftwidth=4:
