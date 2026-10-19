# Copyright 2026 Escodoo
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Document Page Markdown",
    "summary": "Insert Markdown written content in knowledge pages",
    "version": "16.0.1.0.0",
    "category": "Knowledge Management",
    "author": "Escodoo, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/knowledge",
    "license": "AGPL-3",
    "development_status": "Alpha",
    "maintainers": ["CristianoMafraJunior"],
    "depends": ["document_page"],
    "external_dependencies": {"python": ["markdown"]},
    "assets": {
        "web.assets_backend": [
            "document_page_markdown/static/src/js/markdown_dialog.esm.js",
            "document_page_markdown/static/src/js/markdown_powerbox.esm.js",
            "document_page_markdown/static/src/xml/markdown_dialog.xml",
            "document_page_markdown/static/src/scss/markdown_dialog.scss",
        ],
        "web.assets_tests": [
            "document_page_markdown/static/tests/tours/markdown_powerbox_tour.esm.js",
        ],
    },
}
