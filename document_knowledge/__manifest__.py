# -*- coding: utf-8 -*-
# Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Knowledge Management System",
    "version": "10.0.1.0.0",
    "author": "OpenERP SA, MONK Software, Odoo Community Association (OCA)",
    "category": "Knowledge",
    "license": "AGPL-3",
    "website": "https://odoo-community.org/",
    "depends": ["base"],
    "data": [
        "data/ir_module_category.xml",
        "security/knowledge_security.xml",
        "views/knowledge.xml",
        "views/res_config.xml",
    ],
    "demo": ["demo/knowledge.xml"],
    "installable": True,
    "auto_install": False,
}
