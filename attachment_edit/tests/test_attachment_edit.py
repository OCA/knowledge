# -*- coding: utf-8 -*-
# Copyright 2018 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import SUPERUSER_ID
from odoo.tests.common import TransactionCase


class TestAttachmentEdit(TransactionCase):
    def test_attachment_edit(self):
        attachment = self.env['ir.attachment'].create({
            'name': 'attachment',
        })
        self.assertFalse(attachment.res_reference)
        attachment.write({
            'res_model': 'res.users',
            'res_id': SUPERUSER_ID,
        })
        self.assertEqual(
            attachment.res_reference, self.env.ref('base.user_root'),
        )
        attachment.res_reference = None
        self.assertFalse(attachment.res_model)
        self.assertFalse(attachment.res_id)
        attachment.res_reference = self.env.ref('base.user_root')
        self.assertEqual(attachment.res_model, 'res.users')
        self.assertEqual(attachment.res_id, SUPERUSER_ID)
