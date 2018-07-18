# -*- coding: utf-8 -*-
# Copyright 2015-2018 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from psycopg2 import IntegrityError
from openerp.tests.common import TransactionCase
from openerp.tools.misc import mute_logger


class TestDocumentPageTags(TransactionCase):
    def test_document_page_tags(self):
        testtag = self.env['document.page.tag'].name_create('test')
        # check we're charitable on duplicates
        self.assertEqual(
            testtag, self.env['document.page.tag'].name_create('Test'),
        )
        # check we can't create nonunique tags
        with self.assertRaises(IntegrityError):
            with mute_logger('odoo.sql_db'):
                testtag2 = self.env['document.page.tag'].create({
                    'name': 'test2',
                })
                testtag2.write({'name': 'test'})
