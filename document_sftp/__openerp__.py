# -*- coding: utf-8 -*-
# © 2016 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "SFTP",
    "version": "8.0.1.0.0",
    "author": "Therp BV,Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "category": "Knowledge Management",
    "summary": "Access your documents via SFTP",
    "depends": [
        'base',
    ],
    "demo": [
        "demo/res_users.xml",
    ],
    "data": [
        "demo/res_users.xml",
        "views/res_users.xml",
        "data/ir_config_parameter.xml",
    ],
    "post_init_hook": 'post_init_hook',
    "external_dependencies": {
        'python': ['paramiko'],
    },
}
