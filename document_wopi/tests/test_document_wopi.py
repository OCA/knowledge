# -*- coding: utf-8 -*-
# © 2017 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from base64 import b64encode
from openerp.tests.common import TransactionCase
from openerp.exceptions import AccessError
from openerp.tools import mute_logger


class TestDocumentWopi(TransactionCase):
    def test_document_wopi(self):
        config = self.env['knowledge.config.settings'].create({})
        self.assertEqual(
            config.document_wopi_client,
            self.env['ir.config_parameter'].get_param('document_wopi.client'),
        )
        config.set_document_wopi_client()
        discovery = self.env['document.wopi']._discovery()
        self.assertIn(('odt', 'edit'), discovery)

        attachment = self.env['ir.attachment'].create({
            'name': 'testattachment',
            'type': 'binary',
            'datas': b64encode('hello world'),
            'datas_fname': 'testattachment.fodt',
        })

        demo_user = self.env.ref('base.user_demo')
        with mute_logger('openerp.addons.base.ir.ir_model'):
            with self.assertRaises(AccessError):
                token = self.env['document.wopi.access.token'].sudo(
                    demo_user
                )._get_token(attachment)
        token = self.env['document.wopi.access.token']._get_token(attachment)
        self.assertTrue(token.action_url)
        self.assertTrue(
            self.env['document.wopi.access.token']
            ._verify_token(token.token)
        )
        self.assertFalse(
            self.env['document.wopi.access.token'].sudo(demo_user)
            ._verify_token(token.token)
        )
        demo_user.write({
            'groups_id': [
                (4, self.env.ref('attachment_lock.group_attachment_lock').id),
            ],
        })
        token = self.env['document.wopi.access.token'].sudo(
            demo_user
        )._get_token(attachment)
        self.assertTrue(token)
        self.assertTrue(
            self.env['document.wopi.access.token'].sudo(demo_user)
            ._verify_token(token.token)
        )
