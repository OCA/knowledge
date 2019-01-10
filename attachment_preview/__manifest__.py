# Copyright 2014 Therp BV (<http://therp.nl>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Preview attachments",
    "version": "11.0.1.3.0",
    "author": "Therp BV,"
              "Onestein,"
              "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "summary": 'Preview attachments supported by Viewer.js',
    "category": "Knowledge Management",
    "depends": [
        'web',
    ],
    "data": [
        "templates/assets.xml",
    ],
    "qweb": [
        'static/src/xml/attachment_preview.xml',
    ],
    "installable": True,
}
