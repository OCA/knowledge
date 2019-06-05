# -*- coding: utf-8 -*-
# Copyright 2018 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from base64 import b64encode
from openerp.tests.common import TransactionCase
from openerp.exceptions import AccessError, ValidationError


class TestAttachmentLock(TransactionCase):
    def test_attachment_lock(self):
        demo = self.env.ref('base.user_demo')
        testattachment = self.env['ir.attachment'].create({
            'name': 'testattachment',
            'datas': b64encode('hello world'),
            'datas_fname': 'test.txt',
        })
        self.assertTrue(testattachment.can_lock)
        self.assertFalse(testattachment.locked)
        testattachment.lock()
        self.assertTrue(testattachment.can_lock)
        self.assertTrue(testattachment.locked)
        with self.assertRaises(ValidationError):
            testattachment.sudo(demo).write({
                'datas': b64encode('hello world2'),
            })
        with self.assertRaises(AccessError):
            testattachment.sudo(demo).lock()
        demo.write({'groups_id': [
            (4, self.env.ref('attachment_lock.group_attachment_lock').id),
        ]})
        with self.assertRaises(AccessError):
            testattachment.sudo(demo).lock()
        testattachment.unlock()
        self.assertTrue(testattachment.sudo(demo).can_lock)
        testattachment.sudo(demo).lock()
        self.assertTrue(testattachment.sudo(demo).can_lock)
        self.assertTrue(testattachment.sudo(demo).locked)
