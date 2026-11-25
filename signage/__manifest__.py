# Copyright (C) 2025 Dimitrios Tanis (<dtanis@tanisfood.gr>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Signage",
    "summary": "Base module to create signs",
    "version": "18.0.1.0.0",
    "category": "Knowledge Management",
    "website": "https://github.com/OCA/knowledge",
    "author": "Dimitrios Tanis, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": [
        "document_page",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/signage_view.xml",
        "views/signage_category_view.xml",
    ],
}
