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
    'version': '8.0.1.0.0',
    "author": "Savoir-faire Linux,Odoo Community Association (OCA)",
    "website": "http://www.savoirfairelinux.com",
    "license": "AGPL-3",
    'category': 'Knowledge Management',
    'description': """
This module adds a workflow to approve page modification and show the approved
version by default.

Scenario
========

* Set a valid email address on the company settings.
* Create a new page category and set an approver group. Make sure users
  belonging to that group have valid email addresses.
* Create a new page and choose the previously created category.
* A notification is sent to the group with a link to the page history to
  review.
* Depending on the review, the page history is approved or not.
* Users reading the page see the last approved version.
    """,
    'depends': [
        'knowledge',
        'document_page',
        'email_template',
    ],
    'data': [
        'data/email_template.xml',
        'document_page_wkfl.xml',
        'document_page_view.xml',
        'security/document_page_security.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'auto_install': False,
    'images': [
        'images/category.png',
        'images/page_history_list.png',
        'images/page_history.png',
    ],
}
