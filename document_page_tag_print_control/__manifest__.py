# Copyright 2025 Juan Alberto Raja <juan.raja@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Document Page Tag Print Control",
    "summary": "Restricts document page printing based on assigned tags",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "author": "Sygel, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/knowledge",
    "category": "Knowledge",
    "depends": [
        "document_page_tag",
    ],
    "data": [
        "views/document_page_tag.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}
