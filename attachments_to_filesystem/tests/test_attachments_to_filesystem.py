# -*- coding: utf-8 -*-
# © 2017 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp.tests.common import TransactionCase


class TestAttachmentsToFilesystem(TransactionCase):
    def test_attachments_to_filesystem(self):
        # given the init function was run for the asynchronous behavior
        # already, we just need to test synchronous behavior
        self.env['ir.config_parameter'].set_param(
            'attachments_to_filesystem.move_during_init', 'yes'
        )
        self.env['ir.attachment']._attachments_to_filesystem_cron()
        self.assertFalse(
            self.env.ref('attachments_to_filesystem.test_attachment').db_datas
        )
        self.assertTrue(
            self.env.ref(
                'attachments_to_filesystem.test_attachment_unknown_model'
            ).db_datas
        )
