# Copyright (C) 2020 Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Document Tag",
    "version": "13.0.1.0.0",
    "category": "Knowledge Management",
    "author": "Open Source Integrators, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/knowledge",
    "license": "AGPL-3",
    "depends": ["document_page"],
    "data": [
        "security/ir.model.access.csv",
        "security/ir_rule.xml",
        "views/document_tag.xml",
        "views/document_page.xml",
    ],
    "development_status": "Beta",
    "maintainers": ["max3903"],
}
