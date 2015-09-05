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
import base64
from openerp.tests.common import TransactionCase


class TestReindex(TransactionCase):
    def test_reindex(self):
        '''test if the indexer indexes what we want to index and only that'''
        # we do this to avoid error messages about word files in demo data
        self.env['ir.attachment'].search([]).unlink()
        att1 = self.env['ir.attachment'].create({
            'name': 'helloworld1.txt',
            'datas_fname': 'helloworld1.txt',
            'datas': base64.b64encode('hello'),
        })
        att2 = self.env['ir.attachment'].create({
            'name': 'helloworld2.txt',
            'datas_fname': 'helloworld2.txt',
            'datas': base64.b64encode('world'),
        })
        self.assertEqual(att1.file_type, 'text/plain')
        self.assertEqual(att2.file_type, 'text/plain')
        att1.write({'index_content': False})
        att2.write({'index_content': 'hello'})
        self.env['ir.attachment'].document_reindex_unindexed()
        self.assertEqual(att1.index_content, 'hello')
        self.assertEqual(att2.index_content, 'hello')
        self.env['ir.attachment'].document_reindex_all()
        self.assertEqual(att2.index_content, 'world')
