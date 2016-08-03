# -*- coding: utf-8 -*-
# © 2016 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import logging
import socket
import StringIO
import threading
from openerp import SUPERUSER_ID, api, models
from openerp.modules.registry import RegistryManager
try:
    import paramiko
    from ..document_sftp_transport import DocumentSFTPTransport
    from ..document_sftp_server import DocumentSFTPServer
    from ..document_sftp_sftp_server import DocumentSFTPSftpServerInterface,\
        DocumentSFTPSftpServer
except ImportError:   # pragma: no cover
    pass
_db2thread = {}
_channels = []
_logger = logging.getLogger(__name__)


class DocumentSFTP(models.AbstractModel):
    _name = 'document.sftp'
    _description = 'SFTP server'

    def _run_server(self, dbname, stop):
        with api.Environment.manage():
            with RegistryManager.get(dbname).cursor() as cr:
                env = api.Environment(cr, SUPERUSER_ID, {})
                env[self._name].__run_server(stop)

    @api.model
    def __run_server(self, stop):
        # this is heavily inspired by
        # https://github.com/rspivak/sftpserver/blob/master/src/sftpserver
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        host, port = self.env['ir.config_parameter'].get_param(
            'document_sftp.bind', 'localhost:0'
        ).split(':')
        _logger.info('Binding to %s:%s', host, port)
        server_socket.bind((host, int(port)))
        host_real, port_real = server_socket.getsockname()
        _logger.info(
            'Listening to SFTP connections on %s:%s', host_real, port_real)
        if host_real != host or port_real != port:
            self.env['ir.config_parameter'].set_param(
                'document_sftp.bind', '%s:%s' % (host_real, port_real))
        server_socket.listen(5)
        server_socket.settimeout(2)

        while not stop.is_set():
            try:
                conn, addr = server_socket.accept()
            except socket.timeout:
                while _channels and\
                        not _channels[0].get_transport().is_active():
                    _channels.pop(0)
                continue

            _logger.debug('Accepted connection from %s', addr)

            key = StringIO.StringIO(self.env['ir.config_parameter'].get_param(
                'document_sftp.hostkey'))
            host_key = paramiko.ecdsakey.ECDSAKey.from_private_key(key)
            key.close()
            transport = DocumentSFTPTransport(self.env.cr.dbname, conn)
            transport.add_server_key(host_key)
            transport.set_subsystem_handler(
                'sftp', DocumentSFTPSftpServer,
                DocumentSFTPSftpServerInterface, self.env)

            server = DocumentSFTPServer(self.env)
            try:
                transport.start_server(server=server)
                channel = transport.accept()
                if channel:
                    _channels.append(channel)
            except (paramiko.SSHException, EOFError):
                continue

    @api.model
    def _get_root_handlers(self):
        return [
            self.env['document.sftp.root.by_model'],
        ]

    @api.model
    def _get_root_entries(self):
        entries = []
        for model in self._get_root_handlers():
            entries.append(model._get_root_attributes())
        return entries

    @api.model
    def _get_handler_for(self, path):
        # TODO: this can be smarter
        return self.env['document.sftp.root.by_model']

    def _register_hook(self, cr):
        if cr.dbname not in _db2thread:
            stop = threading.Event()
            _db2thread[cr.dbname] = (
                threading.Thread(
                    target=self._run_server, args=(cr.dbname, stop)),
                stop,
            )
            _db2thread[cr.dbname][0].start()
            from openerp.service.server import server
            old_stop = server.stop

            def new_stop():
                stop.set()
                old_stop()

            server.stop = new_stop
        return super(DocumentSFTP, self)._register_hook(cr)
