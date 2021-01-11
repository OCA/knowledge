# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


class TestDocumentPageReferenceSearch(TransactionCase):

    def setUp(self):
        super().setUp()
        self.partner_id = self.env['res.partner'].create({
            'name': 'Contact',
            'ref': 'REF1'
        })
        res_partner = self.env['ir.model'].search(
            [('model', '=', 'res.partner')]
        )
        ref_field = self.env['ir.model.fields'].search(
            [('model_id', '=', res_partner.id), ('name', '=', 'ref')]
        )
        self.rule = self.env['document.page.reference.rule'].create({
            'name': 'RULE',
            'model_id': res_partner.id,
            'field_id': ref_field.id
        })
        self.page_1 = self.env['document.page'].create({
            'name': 'Page 1'
        })

    def test_document_page_reference_search(self):
        separator = self.env['ir.config_parameter'].get_param(
            'document.reference.separator'
        )
        code_1 = 'R%sREF1' % separator
        result = self.env['document.page']._get_document(code_1)
        self.assertFalse(result)

        code_2 = 'RULE%sREF2'
        result = self.env['document.page']._get_document(code_2)
        self.assertFalse(result)

        code_3 = 'RULE%sREF1' % separator
        result = self.env['document.page']._get_document(code_3)
        self.assertEqual(result, self.partner_id)

        with self.assertRaises(ValidationError):
            test_ref = 'Test%sref' % separator
            self.page_1.write({
                'reference': test_ref
            })
        self.rule.onchange_model()
        self.assertFalse(self.rule.field_id)
