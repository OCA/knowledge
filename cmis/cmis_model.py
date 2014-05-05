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
from cmislib.model import CmisClient
import cmislib.exceptions


class cmis_backend(orm.Model):
    _name = 'cmis.backend'
    _description = 'CMIS Backend'
    _inherit = 'connector.backend'

    _backend_type = 'cmis'

    def _select_versions(self, cr, uid, context=None):
        return [('1.0', '1.0')]

    # Test connection with GED
    def _auth(self, cr, uid, context=None):
        if context is None:
            context = {}
        # Get the url, user and password for GED
        ids = self.search(cr, uid, [])
        res = self.read(cr, uid, ids,
                        ['location',
                         'username',
                         'password'], context=context)[0]
        url = res['location']
        user_name = res['username']
        user_password = res['password']
        client = CmisClient(url, user_name, user_password)
        try:
            return client.defaultRepository
        except cmislib.exceptions.ObjectNotFoundException:
            raise orm.except_orm(_('Cmis connection Error!'),
                                 _("Check your cmis account configuration."))
        except cmislib.exceptions.PermissionDeniedException:
            raise orm.except_orm(_('Cmis connection Error!'),
                                 _("Check your cmis account configuration."))

    def check_directory_of_write(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        cmis_backend_obj = self.pool.get('cmis.backend')
        datas_fname = 'testdoc'
        # login with the cmis account
        repo = self._auth(cr, uid, context=context)

        folder_path_write = cmis_backend_obj.read(
            cr, uid, ids, ['initial_directory_write'],
            context=context)[0]['initial_directory_write']
        # Testing the path
        rs = repo.query("SELECT cmis:path FROM  cmis:folder")
        bool_path_write = self.check_existing_path(rs, folder_path_write)
        # Check if we can create a doc from OE to EDM
        # Document properties
        if bool_path_write:
            sub = repo.getObjectByPath(folder_path_write)
            sub.createDocumentFromString(
                datas_fname,
                contentString='hello, world',
                contentType='text/plain')
        self.get_error_for_path(bool_path_write, folder_path_write)

    def check_directory_of_read(self, cr, uid, ids, context=None):
        ir_attach_obj = self.pool.get('ir.attachment')
        if context is None:
            context = {}
        cmis_backend_obj = self.pool.get('cmis.backend')
        # login with the cmis account
        repo = self._auth(cr, uid, context=context)
        folder_path_read = cmis_backend_obj.read(
            cr, uid, ids, ['initial_directory_read'],
            context=context)[0]['initial_directory_read']
        # Testing the path
        rs = repo.query("SELECT cmis:path FROM  cmis:folder ")
        bool_path_read = self.check_existing_path(rs, folder_path_read)
        file_name = 'testdoc'
        # Add testdoc in the context just to check if it is as test
        context['bool_testdoc'] = True
        if bool_path_read:
            # Get results from name of document
            results = repo.query(" SELECT * FROM  cmis:document \
                         WHERE cmis:name LIKE '%" + file_name + "%'")
            for result in results:
                info = result.getProperties()
                data_attach = {
                    'name': info['cmis:name'],
                    'datas_fname': info['cmis:name'],
                    'type': 'binary',
                    'datas': result.getContentStream().read().encode('base64'),
                }
                ir_attach_obj.create(cr, uid, data_attach, context=context)
        self.get_error_for_path(bool_path_read, folder_path_read)

    def check_existing_path(self, rs, folder_path):
        for one_rs in rs:
            # Print name of files
            props = one_rs.getProperties()
            if props['cmis:path'] != folder_path:
                bool = False
            else:
                bool = True
                break
        return bool

    def get_error_for_path(self, bool, path):
        if bool:
            raise orm.except_orm(_('Cmis  Message'),
                                 _("Path is correct for : " + path))
        else:
            raise orm.except_orm(_('Cmis  Error!'),
                                 _("Error path for : " + path))

    _columns = {
        'version': fields.selection(
            _select_versions,
            string='Version',
            required=True),
        'location': fields.char('Location', size=128, help="Location."),
        'username': fields.char('Username', size=64, help="Username."),
        'password': fields.char('Password', size=64, help="Password."),
        'initial_directory_read': fields.char(
            'Initial directory of read',
            size=128,
            help="Initial directory of read."),
        'initial_directory_write': fields.char(
            'Initial directory of write',
            size=128,
            help="Initial directory of write."),
    }
    _default = {
        'initial_directory_read': '/',
        'initial_directory_write': '/',
    }

# vim:expandtab:smartindent:toabstop=4:softtabstop=4:shiftwidth=4:
