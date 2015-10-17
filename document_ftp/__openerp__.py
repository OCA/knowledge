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


{
    'name': 'Shared Repositories (FTP)',
    'version': '8.0.0.0.1',
    'category': 'Knowledge Management',
    'author': 'Odoo Community Association (OCA)',
    "license": "AGPL-3",
    'website': 'http://www.openerp.com',
    'depends': ['base', 'document'],
    'data': [
        'wizard/ftp_configuration_view.xml',
        'wizard/ftp_browse_view.xml',
        'security/ir.model.access.csv',
        'res_config_view.xml',
    ],
    'demo': [],
    'test': [
        'test/document_ftp_test2.yml',
        'test/document_ftp_test4.yml',
    ],
    'installable': True,
    'auto_install': False,
    'images': ['images/1_configure_ftp.jpeg',
               'images/2_document_browse.jpeg',
               'images/3_document_ftp.jpeg'],
    'post_load': 'post_load',
}

