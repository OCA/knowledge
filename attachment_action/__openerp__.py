# -*- coding: utf-8 -*-
# Copyright 2018 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Actions on attachments",
    "version": "8.0.1.0.0",
    "author": "Therp BV,Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "category": "Hidden/Dependency",
    "summary": "Enable/disable actions on attachments",
    "depends": [
        'web',
        'knowledge',
        'document',
    ],
    "data": [
        'views/templates.xml',
    ],
    "qweb": [
        'static/src/xml/attachment_action.xml',
    ],
}
