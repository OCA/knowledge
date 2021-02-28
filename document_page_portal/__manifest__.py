# Copyright (C) 2020 - TODAY, Marcel Savegnago - Escodoo).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


{
    "name": "Document Page Portal",
    "summary": """
        This module enables document page portal""",
    "version": "13.0.1.0.0",
    "category": "Knowledge Management",
    "author": "Escodoo, Odoo Community Association (OCA)",
    "maintainers": ["marcelsavegnago"],
    "images": ["static/description/banner.png"],
    "website": "https://github.com/OCA/knowledge",
    "license": "AGPL-3",
    "depends": ["base", "portal", "document_page"],
    "data": [
        "views/assets.xml",
        "views/document_page.xml",
        "security/document_page_portal_security.xml",
        "security/ir.model.access.csv",
        "views/document_page_portal_templates.xml",
    ],
}
