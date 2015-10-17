# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).

#    ThinkOpen Solutions Brasil (<https://tkobr.com>).
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
##############################################################################

import threading
import logging

import document_ftp.ftpserver.Authorizer
import document_ftp.ftpserver.AbstractedFs
import document_ftp.ftpserver.FtpServer

import openerp
from openerp.tools import config
_logger = logging.getLogger(__name__)
import socket


def start_server():
    if openerp.multi_process:
        _logger.info("FTP disabled in multiprocess mode")
        return
    ip_address = ([(s.connect(('8.8.8.8', 80)), s.getsockname()[0], s.close()) 
           for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1])
    if not ip_address:
        ip_address = '127.0.0.1'
    HOST = config.get('ftp_server_host', str(ip_address))
    PORT = int(config.get('ftp_server_port', '8021'))
    PASSIVE_PORTS = None
    pps = config.get('ftp_server_passive_ports', '').split(':')
    if len(pps) == 2:
        PASSIVE_PORTS = int(pps[0]), int(pps[1])

    class FtpServer(threading.Thread):

        def run(self):
            autho = Authorizer.Authorizer()
            FtpServer.FTPHandler.Authorizer = autho
            FtpServer.max_cons = 300
            FtpServer.max_cons_per_ip = 50
            FtpServer.FTPHandler.AbstractedFs = AbstractedFs.AbstractedFs
            if PASSIVE_PORTS:
                FtpServer.FTPHandler.passive_ports = PASSIVE_PORTS

            FtpServer.log = lambda msg: _logger.info(msg)
            FtpServer.logline = lambda msg: None
            FtpServer.logerror = lambda msg: _logger.error(msg)

            ftpd = FtpServer.FTPServer((HOST, PORT), FtpServer.FTPHandler)
            ftpd.serve_forever()

    if HOST.lower() == 'none':
        _logger.info("\n Server FTP Not Started\n")
    else:
        _logger.info("\n Serving FTP on %s:%s\n" % (HOST, PORT))
        ds = FtpServer()
        ds.daemon = True
        ds.start()