# -*- coding: utf-8 -*-
# © 2017 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "WOPI",
    "version": "8.0.1.0.0",
    "author": "Therp BV,Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "category": "Knowledge Management",
    "summary": "Allow online collaborative editing of your documents",
    "depends": [
        'knowledge',
        'attachment_action',
        'attachment_lock',
    ],
    "demo": [
        "demo/ir_config_parameter.xml",
    ],
    "data": [
        "security/ir_rule.xml",
        "data/ir_actions_todo.xml",
        "views/knowledge_config_settings.xml",
        'views/templates.xml',
        'security/ir.model.access.csv',
    ],
    "qweb": [
        "static/src/xml/document_wopi.xml",
    ],
    "images": [
        "images/screenshot.png",
    ],
}
