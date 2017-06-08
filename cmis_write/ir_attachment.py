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
from openerp.addons.connector.session import ConnectorSession
from openerp.addons.connector.queue.job import job
import base64
from openerp import SUPERUSER_ID
from openerp.tools.translate import _
import logging
_logger = logging.getLogger(__name__)


class ir_attachment_download(orm.TransientModel):
    _name = 'ir.attachment.download'

    _columns = {
        'name': fields.char('Attachment Name', size=256, required=True,
                            help='Attachment Name'),
        'datas': fields.binary('File', readonly=True),
        'type': fields.char('Type', size=256, help='Type'),
        'file_type': fields.char('Content Type', help='Content Type'),
        'attachment_id':  fields.many2one('ir.attachment', 'Attachment'),
    }
    _defaults = {
        'type': 'binary',
    }


class ir_attachment(orm.Model):
    _inherit = 'ir.attachment'

    def create(self, cr, uid, values, context=None):
        metadata_obj = self.pool.get('metadata')
        user_obj = self.pool.get('res.users')
        user_login = user_obj.browse(cr, uid, uid, context=context).login
        session = ConnectorSession(cr, uid, context=context)
        value = {
            'name': values.get('name'),
            'datas_fname': values.get('datas_fname'),
            'file_type': values.get('file_type') or '',
            'datas': values.get('datas'),
            'description': values.get('description') or '',

        }

        metadata_ids = metadata_obj.search(cr, uid, [], context=context)
        dict_metadata = {}
        list_fields = []
        # Get list of metadata
        if values.get('res_model'):
            for line in metadata_obj.browse(cr, uid, metadata_ids,
                                            context=context):
                if line.model_id.model == values.get('res_model'):
                    if line.metadata_list_ids:
                        for one_field in line.metadata_list_ids:
                            list_fields.append(one_field.field_id.name)
            result = self.pool.get(values.get('res_model')).read(cr, uid, [
                values.get('res_id')], list_fields, context=context)[0]

            for one_field in list_fields:
                dict_metadata['cmis:' + one_field] = result[one_field]
        values['datas'] = None
        res = super(ir_attachment, self).create(cr, uid, values,
                                                context=context)
        # Create Job
        # if bool_testdoc in context, we don't need to create
        # the doc in the DMS
        if not context.get('bool_testdoc'):
            create_doc_in_edm.delay(
                session, 'ir.attachment', value, res, dict_metadata,
                user_login)
        return res

    def action_download(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        cmis_backend_obj = self.pool.get('cmis.backend')
        # login with the cmis account
        repo = cmis_backend_obj._auth(cr, uid, context=context)
        cmis_backend_rec = self.read(
            cr, uid, ids, ['id_dms'], context=context)[0]
        id_dms = cmis_backend_rec['id_dms']
        # Get results from id of document
        results = repo.query(" SELECT * FROM  cmis:document WHERE \
                             cmis:objectId ='" + id_dms + "'")
        datas = results[0].getContentStream().read().encode('base64')
        return datas

    def _data_set(self, cr, uid, id, name, value, arg, context=None):
        # We dont handle setting data to null
        if not value:
            return True
        if context is None:
            context = {}
        location = self.pool.get('ir.config_parameter').get_param(
            cr, uid, 'ir_attachment.location')
        file_size = len(value.decode('base64'))
        if location:
            attach = self.browse(cr, uid, id, context=context)
            if attach.store_fname:
                self._file_delete(cr, uid, location, attach.store_fname)
            fname = self._file_write(cr, uid, location, value)
            # SUPERUSER_ID as probably don't have write access,
            # trigger during create
            super(ir_attachment, self).write(
                cr, SUPERUSER_ID, [id],
                {'store_fname': fname, 'file_size': file_size},
                context=context)
        else:
            super(ir_attachment, self).write(
                cr, SUPERUSER_ID, [id],
                {'db_datas': value, 'file_size': file_size}, context=context)
        return True

    def _data_get(self, cr, uid, ids, name, arg, context=None):
        if context is None:
            context = {}
        result = {}
        location = self.pool.get('ir.config_parameter').get_param(
            cr, uid, 'ir_attachment.location')
        bin_size = context.get('bin_size')
        for attach in self.browse(cr, uid, ids, context=context):
            if location and attach.store_fname:
                result[attach.id] = self._file_read(
                    cr, uid, location, attach.store_fname, bin_size)
            elif attach.id_dms:
                datas = self.action_download(
                    cr, uid, attach.id, context=context)
                result[attach.id] = datas
                file_type, index_content = self._index(
                    cr, uid, datas.decode('base64'), attach.datas_fname, None)
                self.write(
                    cr, uid, [attach.id],
                    {'file_type': file_type, 'index_content': index_content},
                    context=context)
            else:
                raise orm.except_orm(_('Access error of document'),
                                     _("Document is not available in DMS; "
                                       "Please try again"))
        return result

    _columns = {
        'id_dms': fields.char('Id of Dms', size=256, help="Id of Dms."),
        'download_id': fields.one2many('ir.attachment.download',
                                       'attachment_id',
                                       'Attachment download'),
        'datas': fields.function(_data_get, fnct_inv=_data_set,
                                 string='File Content',
                                 type="binary", nodrop=True),
    }


@job
def create_doc_in_edm(session, model_name, value, res,
                      dict_metadata, user_login, filters=None):
    ir_attach_obj = session.pool.get('ir.attachment')
    cmis_backend_obj = session.pool.get('cmis.backend')
    if session.context is None:
        session.context = {}
    # login with the cmis account
    repo = cmis_backend_obj._auth(session.cr, session.uid,
                                  context=session.context)
    root = repo.rootFolder
    ids = cmis_backend_obj.search(session.cr, session.uid, [], session.context)

    folder_path = cmis_backend_obj.read(
        session.cr, session.uid,
        ids,
        ['initial_directory_write'],
        context=session.context)[0]['initial_directory_write']
    # Document properties
    if value['name']:
        file_name = value['name']
    elif value['datas_fname']:
        file_name = value['datas_fname']
    else:
        file_name = value['datas_fname']
    props = {
        'cmis:name': file_name,
        'cmis:description': value['description'],
        'cmis:createdBy': user_login,
    }
    # Add list of metadata in props
    if len(dict_metadata):
        for k, v in dict_metadata.iteritems():
            props[k] = v
    if folder_path:
        sub1 = repo.getObjectByPath(folder_path)
    else:
        sub1 = root
    someDoc = sub1.createDocumentFromString(file_name,
                                            contentString=base64.b64decode(
                                                value['datas']),
                                            contentType=value['file_type'])
    # TODO: create custom properties on a document (Alfresco)
    # someDoc.getProperties().update(props)
    # Updating ir.attachment object with the new id
    # of document generated by DMS
    ir_attach_obj.write(session.cr, session.uid, res, {
        'id_dms': someDoc.getObjectId()}, session.context)
    return True

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
