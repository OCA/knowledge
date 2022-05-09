# Copyright 2022 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Document Page Access Group",
    "summary": "Choose groups to access document pages",
    "version": "14.0.1.0.0",
    "category": "Knowledge",
    "website": "https://github.com/OCA/knowledge",
    "author": "Sygel, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "document_page",
        "knowledge",
    ],
    "data": ["views/document_page.xml", "security/security.xml"],
}
