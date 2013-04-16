# -*- encoding: utf-8 -*-
##############################################################################
#    
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2013 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
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
    'name': 'Document Page Approval',
    'version': '1.0',
    "author" : "Savoir-faire Linux",
    "website" : "http://www.savoirfairelinux.com",
    "license" : "AGPL-3",
    'category': 'Knowledge Management',
    'description': """
Add a workflow to approve page modification and show the approved version by default
    """,
    'depends': ['document_page', 'email_template'],
    'update_xml': ['document_page_wkfl.xml','document_page_view.xml'],
    'installable': True,
    'auto_install': False,
    'images': [],
    'data': [
        'security/document_page_security.xml',
        'security/ir.model.access.csv',
        ]
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
