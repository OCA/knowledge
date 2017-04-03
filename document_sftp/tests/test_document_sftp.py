# -*- coding: utf-8 -*-
# © 2016 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import time
import paramiko
from openerp import tools
from openerp.modules.registry import RegistryManager
from openerp.tests.common import TransactionCase
from ..models.document_sftp import _db2thread
from ..hooks import post_init_hook


class TestDocumentSftp(TransactionCase):
    def test_document_sftp(self):
        # without this, your ssh thread gets a real registry with blocks
        RegistryManager.enter_test_mode()
        # be sure to set a hostkey
        post_init_hook(self.env.cr, self.registry)
        self.assertTrue(
            'PRIVATE KEY' in
            self.env['ir.config_parameter'].get_param('document_sftp.hostkey')
        )
        # be sure to start our server
        self.env['document.sftp']._register_hook()
        # give it some time
        time.sleep(5)
        # use this to bind to our server
        bind = self.env['ir.config_parameter'].get_param('document_sftp.bind')
        host, port = bind.split(':')
        transport = paramiko.Transport((host, int(port)))
        demo_key = paramiko.rsakey.RSAKey(
            file_obj=tools.file_open('document_sftp/demo/demo.key'))
        transport.connect(username='demo', pkey=demo_key)

        sftp = paramiko.SFTPClient.from_transport(transport)
        self.assertTrue('By model' in sftp.listdir('.'))
        self.assertTrue('res.company' in sftp.listdir('/By model'))
        sftp.close()
        # we need to stop our thread before leaving test mode, otherwise: lock
        thread = _db2thread[self.env.cr.dbname][0]
        _db2thread[self.env.cr.dbname][1].set()
        thread.join()
        RegistryManager.leave_test_mode()
