# -*- coding: utf-8 -*-
###############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 Savoir-faire Linux (<http://www.savoirfairelinux.com>)
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


class test_ir_attachment(TransactionCase):

    def setUp(self):
        super(test_ir_attachment, self).setUp()

        # Get registries
        self.ira_model = self.registry('ir.attachment')
        self.user_model = self.registry("res.users")
        self.partner_model = self.registry("res.partner")
        self.context = self.user_model.context_get(self.cr, self.uid)

        # Create first partner
        self.partner_id_1 = self.partner_model.create(self.cr, self.uid, {
            'name': 'Test first partner'
        }, context=self.context)

        # Create second partner
        self.partner_id_2 = self.partner_model.create(self.cr, self.uid, {
            'name': 'Test second partner'
        }, context=self.context)

        blob1 = 'blob1'
        blob1_b64 = blob1.encode('base64')

        self.vals = {
            'name': 'Test documemt',
            'datas': blob1_b64,
            'res_model': 'res.partner',
            'res_id': self.partner_id_1,
            'res_name': 'Test first partner',
            'attachment_document_ids': [(0, 0, {
                'res_model': 'res.partner',
                'res_id': self.partner_id_1,
                'res_name': 'Test first partner',
            }),
                (0, 0, {
                    'res_model': 'res.partner',
                    'res_id': self.partner_id_2,
                    'res_name': 'Test second partner',
                })
            ]
        }

    def test_create_document(self):
        """Test create document and check each value in vals variable """
        cr, uid, vals, context = self.cr, self.uid, self.vals, self.context
        ira_id = self.ira_model.create(cr, uid, vals, context=context)
        ira_obj = self.ira_model.browse(cr, uid, ira_id, context=context)
        self.assertEqual(ira_obj.name, vals['name'])
        self.assertEqual(ira_obj.res_id, vals['res_id'])
        self.assertEqual(ira_obj.res_name, vals['res_name'])
        self.assertEqual(ira_obj.res_model, vals['res_model'])
        self.assertEqual(
            ira_obj.attachment_document_ids[0].res_id, self.partner_id_1)
        self.assertEqual(
            ira_obj.attachment_document_ids[0].res_name, 'Test first partner')
        self.assertEqual(
            ira_obj.attachment_document_ids[0].res_model, 'res.partner')

    def test_unlink_document(self):
        """Test normal unlink document """
        cr, uid, vals = self.cr, self.uid, self.vals.copy()
        context = self.context
        ira_id = self.ira_model.create(cr, uid, vals, context=context)
        self.ira_model.unlink(cr, uid, ira_id, context=context)

    def test_unlink_document_drop_down(self):
        """Test unlink from drop-down list in the form view """
        cr, uid, vals = self.cr, self.uid, self.vals.copy()
        context = self.context
        context['multiple_records_res_model'] = 'res.partner'
        context['multiple_records_res_id'] = self.partner_id_1
        ira_id = self.ira_model.create(cr, uid, vals, context=context)
        self.ira_model.unlink(cr, uid, [ira_id], context=context)

    def test_name_get_resname(self):
        """Test _name_get_resname function """
        cr, uid, vals, context = self.cr, self.uid, self.vals, self.context
        ira_id = self.ira_model.create(cr, uid, vals, context=context)
        self.assertEquals(self.ira_model._name_get_resname(
            cr, uid, ira_id, obj=None, method=None,
            context=context)[ira_id], vals['res_name'])

    def test_get_related_model_documents(self):
        cr, uid, vals = self.cr, self.uid, self.vals.copy()
        context = self.context
        context['model'] = 'res.partner'
        context['model_id'] = self.partner_id_1
        ira_id = self.ira_model.create(cr, uid, vals, context=context)
        res = self.ira_model._get_related_model_documents(
            cr, uid, ira_id, field_name=None, args=None, context=context)
        self.assertEqual(res[0], ('id', 'in', [ira_id]))
