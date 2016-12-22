# -*- coding: utf-8 -*-
# Copyright (C) 2013 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Document Page Approval',
    'version': '10.0.1.0.0',
    "author": "Savoir-faire Linux, Odoo Community Association (OCA)",
    "website": "http://www.savoirfairelinux.com",
    "license": "AGPL-3",
    'category': 'Knowledge Management',
    'depends': [
        'document_page',
        'mail',
    ],
    'data': [
        'data/email_template.xml',
        'workflows/document_page_approval.xml',
        'views/document_page_approval.xml',
        'security/document_page_security.xml',
        'security/ir.model.access.csv',
    ],
    'images': [
        'images/category.png',
        'images/page_history_list.png',
        'images/page_history.png',
    ],
}
