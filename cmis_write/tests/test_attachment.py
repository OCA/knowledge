# -*- encoding: utf-8 -*-
###############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2010 - 2014 Savoir-faire Linux
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
###############################################################################

from openerp.tests.common import TransactionCase
from openerp.addons.connector.session import ConnectorSession


class test_attachment(TransactionCase):

    def setUp(self):
        super(test_attachment, self).setUp()
        # Clean up registries
        self.registry('ir.model').clear_caches()
        self.registry('ir.model.data').clear_caches()
        # Get registries
        self.user_model = self.registry("res.users")
        self.ir_attachment_model = self.registry("ir.attachment")
        self.partner_model = self.registry('res.partner')
        self.metadata_model = self.registry('metadata')
        # Get context
        self.context = self.user_model.context_get(self.cr, self.uid)

        partner_id = self.partner_model.create(
            self.cr, self.uid,
            {'name': 'Test Partner',
             'email': 'test@localhost',
             'is_company': True,
             }, context=None)

        blob1 = 'blob1'
        blob1_b64 = blob1.encode('base64')

        self.vals = {
            'name': 'a1',
            'datas': blob1_b64,
            'attachment_document_ids': [(0, 0, {
                'res_model': "res.partner",
                'res_id': partner_id,
                'res_name': 'Test Partner',
            })],
        }

    def test_create_test_attachment(self):
        cr, uid, vals, context = self.cr, self.uid, self.vals, self.context
        vals['datas'] = None
        context['bool_testdoc'] = True
        ir_attachment_id = self.ir_attachment_model.create(
            cr, uid, vals, context=context)
        ir_attachment_pool = self.ir_attachment_model.browse(
            cr, uid, ir_attachment_id, context=context)

        self.assertEqual(ir_attachment_pool.name, vals['name'])
