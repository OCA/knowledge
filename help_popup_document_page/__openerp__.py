# -*- coding: utf-8 -*-
# © 2017 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Document pages for help",
    "version": "8.0.1.0.0",
    "author": "Therp BV,Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "category": "Knowledge Management",
    "summary": "Use document pages as help popup",
    "depends": [
        'document_page',
        'help_popup',
    ],
    "demo": [
        "demo/document_page.xml",
    ],
    "data": [
        "data/document_page.xml",
        "security/res_groups.xml",
        "views/document_page.xml",
    ],
    "post_init_hook": "post_init_hook",
}
