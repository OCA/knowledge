# -*- coding: utf-8 -*-
# Copyright 2018 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Attachment locking",
    "version": "8.0.1.0.0",
    "author": "Therp BV,Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "category": "Knowledge Management",
    "summary": "Support for locks on attachments for external applications",
    "depends": [
        'attachment_action',
    ],
    "data": [
        "security/res_groups.xml",
        "security/ir_rule.xml",
        'security/ir.model.access.csv',
        "views/ir_attachment_lock.xml",
        "data/ir_cron.xml",
        'views/templates.xml',
    ],
    "qweb": [
        'static/src/xml/attachment_lock.xml',
    ],
}
