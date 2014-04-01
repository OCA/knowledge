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

from openerp.osv import orm, fields, osv
from openerp.tools.translate import _
from openerp.addons.connector.queue.job import job
from cmislib.model import CmisClient
import openerp.addons.connector as connector
from openerp.addons.connector.session import ConnectorSession


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
        if not client:
            raise osv.except_osv(_('Cmis connection Error!'),
                                 _("Check your cmis account configuration."))
        return client

    def test_directory_of_write(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        cmis_backend_obj = self.pool.get('cmis.backend')
        #login with the cmis account
        client = cmis_backend_obj._auth(cr, uid, context=context)
        repo = client.defaultRepository
        folder_path_write = cmis_backend_obj.read(cr, uid, ids, ['initial_directory_write'],
                                                  context=context)[0]['initial_directory_write']
        # Testing the path
        rs = repo.query("SELECT cmis:path FROM  cmis:folder ")
        bool_path_write = self.test_existing_path(rs, folder_path_write)
        self.get_error_for_path(bool_path_write, folder_path_write)

    def test_directory_of_read(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        cmis_backend_obj = self.pool.get('cmis.backend')
        #login with the cmis account
        client = cmis_backend_obj._auth(cr, uid, context=context)
        repo = client.defaultRepository
        folder_path_read = cmis_backend_obj.read(cr, uid, ids, ['initial_directory_read'],
                                                 context=context)[0]['initial_directory_read']
        # Testing the path
        rs = repo.query("SELECT cmis:path FROM  cmis:folder ")
        bool_path_read = self.test_existing_path(rs, folder_path_read)
        self.get_error_for_path(bool_path_read, folder_path_read)

    def test_existing_path(self, rs, folder_path):
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
            raise osv.except_osv(_('Cmis  Message'),
                                 _("Path is correct for : " + path))
        else:
            raise osv.except_osv(_('Cmis  Error!'),
                                 _("Error path for : " + path))

    _columns = {
        'version': fields.selection(
            _select_versions,
            string='Version',
            required=True),
        'location': fields.char('Location', size=128, help="Location."),
        'username': fields.char('Username', size=64, help="Username."),
        'password': fields.char('Password', size=64, help="Password."),
        'initial_directory_read': fields.char('Initial directory of read',
                                              size=128, help="Initial directory of read."),
        'initial_directory_write': fields.char('Initial directory of write',
                                               size=128, help="Initial directory of write."),
    }

# vim:expandtab:smartindent:toabstop=4:softtabstop=4:shiftwidth=4:
