# -*- coding: utf-8 -*-
##############################################################################
#
#    This module copyright (C) 2015 Therp BV <http://therp.nl>.
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
from psycopg2 import IntegrityError
from openerp.tests.common import TransactionCase
from ..hooks import post_init_hook


class TestDocumentPageTags(TransactionCase):
    def test_document_page_tags(self):
        # run our init hook for coverage
        post_init_hook(self.cr, self.registry)
        # check we can't create nonunique tags
        with self.assertRaises(IntegrityError):
            self.env['document.page.tag'].name_create('test')
            self.env['document.page.tag'].name_create('test')
