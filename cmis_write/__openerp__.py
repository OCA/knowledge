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
    'name': 'CMIS Write',
    'version': '0.1',
    'category': 'Knowledge Management',
    'summary': 'Create Document in DMS from OpenERP',
    'description': """
Add Documents from OpenERP
==========================

This module allows you to store OpenERP document in the DMS repository.

Configuration
=============

* Create a new CMIS backend with the host, login and password.
* Configure the path in the repository where documents will be dropped.
  By default, it uses the home directory of the user.

Usage
=====

* On one OpenERP record, click "Add document".
* Upload your documents
* Uploaded documents will be enqueued for storage in the DMS

Add Metadata
============

To manage a custom aspect using CMIS (and all the other supported ways)
you have to:

* Define a new custom model configuring Alfresco. To do this I suggest you
http://wiki.alfresco.com/wiki/Step-By-Step:_Creating_A_Custom_Model.

* Add the custom aspect to the document you upload or create in Alfresco.
Using CMIS I suggest you:
http://docs.alfresco.com/4.1/index.jsp?topic=%2Fcom.alfresco.enterprise.doc%2Fconcepts%2Fopencmis-ext-adding.html.

* Set the custom property in the way you probably know using CMIS.

Contributors
------------
* El Hadji Dem (elhadji.dem@savoirfairelinux.com)
""",
    'author': 'Savoir-faire Linux',
    'website': 'www.savoirfairelinux.com',
    'license': 'AGPL-3',
    'depends': [
        'document',
        'cmis',
    ],
    'data': [
        'metadata_view.xml',
        'security/ir.model.access.csv',
    ],
    'js': [
        'static/src/js/document.js'
    ],
    'qweb': [],
    'test': [],
    'demo': [],
    'installable': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
