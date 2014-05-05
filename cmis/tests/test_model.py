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


class test_model(TransactionCase):

    def setUp(self):
        super(test_model, self).setUp()
        # Clean up registries
        self.registry('ir.model').clear_caches()
        self.registry('ir.model.data').clear_caches()
        # Get registries
        self.model = self.registry("cmis.backend")
        # Get context
        self.context = self.model.context_get(self.cr, self.uid)

        self.vals = {
            'name': "Test cmis",
            'version': '1.0',
            'location': "http://localhost:8081/alfresco/s/cmis",
            'username': 'admin',
            'password': 'admin',
        }

    def test_create_model(self):
        model_id = self.model.create(
            self.cr, self.uid, self.vals, context=self.context)
        self.assertTrue(model_id)
