# -*- coding: utf-8 -*-
# © 2016 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp.tests.common import TransactionCase
from openerp.modules.module import get_module_resource


class TestIndexRtf(TransactionCase):

    def test_index_rtf(self):
        """Test if the indexer indexes just the text in rtf documents."""
        attachment_model = self.env['ir.attachment']
        # Force loading of indexer (normally _register_hooks runs after tests)
        attachment_model._register_hook(self.env.cr)
        # we do this to avoid error messages about word files in demo data
        attachment_model.search([]).unlink()
        # Now take rather large rtf test file, with only few actual words:
        rtf_path = get_module_resource(
            'document_rtf_index',
            'test_files',
            'test_with_cat_image.rtf'
        )
        rtf_file = open(rtf_path, 'rb').read().encode('base64')
        att1 = self.env['ir.attachment'].create({
            'name': 'test_with_cat_image.rtf',
            'datas_fname': 'test_with_cat_image.rtf',
            'datas': rtf_file,
        })
        self.assertEqual(att1.file_type, 'application/rtf')
        self.assertEqual(att1.index_content[:16], 'Hello rtf world!')
