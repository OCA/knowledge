# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
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
    "name": "Knowledge Management System",
    "version": "9.0.1.1.0",
    "depends": ["base_setup"],
    "author": "OpenERP SA, Odoo Community Association (OCA)",
    "category": "Hidden/Dependency",
    "license": "AGPL-3",
    "website": "https://www.odoo.com",
    "data": [
        "data/knowledge_data.xml",
        "security/knowledge_security.xml",
        "security/ir.model.access.csv",
        "views/knowledge.xml",
        "views/res_config.xml",
    ],
    "demo": ["demo/knowledge.xml"],
    "installable": True,
    "auto_install": False,
}
