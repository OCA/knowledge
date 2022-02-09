# Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


{
    "name": "Documentation Page",
    "version": "12.0.1.4.0",
    "category": "Knowledge Management",
    "author": "OpenERP SA, Odoo Community Association (OCA)",
    "images": [
        "images/category_list.png",
        "images/create_category.png",
        "images/page_list.png",
        "images/create_page.png",
        "images/customer_invoice.jpeg",
        "images/page_history.png",
    ],
    "website": "https://github.com/OCA/knowledge",
    "license": "AGPL-3",
    "depends": ["mail", "knowledge"],
    "data": [
        "security/document_page_security.xml",
        "security/ir.model.access.csv",
        "wizard/document_page_create_menu.xml",
        "wizard/document_page_show_diff.xml",
        "views/document_page.xml",
        "views/document_page_category.xml",
        "views/document_page_history.xml",
        "views/document_page_assets.xml",
        "views/report_document_page.xml",
    ],
    "demo": ["demo/document_page.xml"],
}
