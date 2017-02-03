# -*- coding: utf-8 -*-
# Copyright 2016 MONK Software
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Force enable attachments",
    "version": "10.0.1.0.0",
    "author": "MONK Software, Odoo Community Association (OCA)",
    "category": "Knowledge",
    "license": "AGPL-3",
    "website": "https://odoo-community.org/",
    "depends": ["document"],
    "data": [
        'templates/web.xml',
    ],
    "qweb": [
        'static/src/xml/sidebar.xml',
    ],
    "installable": True,
    "auto_install": False,
}
