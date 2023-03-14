# Copyright 2014 Therp BV (<http://therp.nl>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Preview attachments",
    "version": "15.0.1.0.0",
    "author": "Therp BV," "Onestein," "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/knowledge",
    "license": "AGPL-3",
    "summary": "Preview attachments supported by Viewer.js",
    "category": "Knowledge Management",
    "depends": ["web", "mail"],
    "data": [],
    "qweb": [],
    "assets": {
        "web._assets_primary_variables": [],
        "web.assets_backend": [
            "attachment_preview/static/src/js/models/attachment_card/attachment_card.esm.js",
            "attachment_preview/static/src/js/attachmentPreviewWidget.esm.js",
            "attachment_preview/static/src/js/components/chatter/chatter.esm.js",
            "attachment_preview/static/src/scss/attachment_preview.scss",
        ],
        "web.assets_frontend": [],
        "web.assets_tests": [],
        "web.qunit_suite_tests": [],
        "web.assets_qweb": ["attachment_preview/static/src/xml/attachment_preview.xml"],
    },
    "installable": True,
}
