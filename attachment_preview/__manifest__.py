# Copyright 2014 Therp BV (<http://therp.nl>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Preview attachments",
    "version": "14.0.1.0.2",
    "author": "Therp BV," "Onestein," "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "summary": "Preview attachments supported by Viewer.js",
    "website": "https://github.com/OCA/knowledge",
    "category": "Knowledge Management",
    "depends": ["web", "mail"],
    "data": ["templates/assets.xml"],
    "qweb": ["static/src/xml/attachment_preview.xml"],
    "installable": True,
}
