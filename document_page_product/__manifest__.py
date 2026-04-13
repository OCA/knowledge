# Copyright 2026 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Document Page Product",
    "summary": "This module links document pages to products",
    "version": "18.0.1.0.0",
    "category": "Product",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/knowledge",
    "license": "AGPL-3",
    "depends": ["product", "document_page"],
    "data": [
        "views/document_page_views.xml",
        "views/product_product_views.xml",
        "views/product_template_views.xml",
    ],
    "installable": True,
    "maintainers": ["victoralmau"],
}
