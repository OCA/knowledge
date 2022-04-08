# Copyright 2014 Tecnativa - Pedro M. Baeza
# Copyright 2020 Tecnativa - Manuel Calero
{
    "name": "URL attachment",
    "version": "15.0.1.0.0",
    "category": "Tools",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/knowledge",
    "license": "AGPL-3",
    "depends": ["mail"],
    "data": ["view/document_url_view.xml", "security/ir.model.access.csv"],
    "assets": {
        "web.assets_backend": [
            "document_url/static/src/js/url.js",
        ],
        "web.assets_qweb": ["document_url/static/src/xml/url.xml"],
    },
    "installable": True,
}
