# -*- coding: utf-8 -*-
# Copyright 2016 MONK Software
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Document Types",
    "version": "10.0.1.0.0",
    "development_status": "Beta",
    "category": "Knowledge",
    "website": "https://github.com/OCA/knowledge",
    "author": "MONK Software, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "auto_install": False,
    "depends": ["document", "knowledge"],
    "data": [
        'views/document_type.xml',
        'views/attachment.xml',
        'templates/web.xml',
        'security/ir.model.access.csv',
    ],
}
