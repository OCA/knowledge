# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2014 Savoir-faire Linux
#    (<http://www.savoirfairelinux.com>).
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
    'name': 'CMIS',
    'version': '0.1',
    'category': 'Connector',
    'summary': 'CMIS Connector',
    'description': """
CMIS Connector
==============

This module is the base for OpenERP modules implementing different integration scenario with a CMIS server.
It allows you to configure a CMIS backend in OpenERP.

Configuration
=============

Create a new CMIS backend with the host, login and password.

Contributors
------------
* El Hadji Dem <elhadji.dem@savoirfairelinux.com>
* Maxime Chambreuil <maxime.chambreuil@savoirfairelinux.com>
""",
    'author': 'Savoir-faire Linux',
    'website': 'www.savoirfairelinux.com',
    'license': 'AGPL-3',
    'depends': [
        'connector',
    ],
    'data': [
        'cmis_model_view.xml',
        'cmis_menu.xml',
    ],
    'js': [],
    'qweb': [],
    'test': [],
    'demo': [],
    'installable': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
