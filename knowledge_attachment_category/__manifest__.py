{
    "name": "Knowledge Attachment Category",
    "summary": "Glue module between knowledge and attachment_category",
    "version": "14.0.1.0.0",
    "category": "Knowledge",
    "website": "https://github.com/OCA/knowledge",
    "author": " Akretion, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "auto_install": True,
    "depends": [
        "knowledge",
        "attachment_category",
    ],
    "data": ["views/knowledge.xml", "views/menu.xml"],
}
