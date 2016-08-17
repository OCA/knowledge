# -*- coding: utf-8 -*-
# © 2016 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import logging
import StringIO
import socket
from lxml import etree
from openerp import SUPERUSER_ID, tools
try:
    from paramiko.ecdsakey import ECDSAKey
except ImportError:  # pragma: no cover
    pass
_logger = logging.getLogger(__name__)


def post_init_hook(cr, pool):
    if socket.getfqdn().endswith('odoo-community.org'):  # pragma: no cover
        # we need a different default listeing address on runbot
        pool['ir.config_parameter'].set_param(
            cr, SUPERUSER_ID, 'document_sftp.bind', '%s:0' % socket.getfqdn())
    hostkey = pool['ir.config_parameter'].get_param(
        cr, SUPERUSER_ID, 'document_sftp.hostkey')
    parameters = etree.parse(
        tools.file_open('document_sftp/data/ir_config_parameter.xml'))
    default_value = None
    for node in parameters.xpath(
        "//record[@id='param_hostkey']//field[@name='value']"
    ):
        default_value = node.text
    if not hostkey or hostkey == default_value:
        _logger.info('Generating host key for database %s', cr.dbname)
        key = StringIO.StringIO()
        ECDSAKey.generate().write_private_key(key)
        pool['ir.config_parameter'].set_param(
            cr, SUPERUSER_ID, 'document_sftp.hostkey', key.getvalue())
        key.close()
