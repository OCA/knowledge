# Copyright 2014 Therp BV (<http://therp.nl>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Preview attachments",
    "version": "16.0.1.0.0",
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
            "attachment_preview/static/src/js/attachmentPreviewWidget.esm.js",
            "attachment_preview/static/src/js/utils.esm.js",
            "attachment_preview/static/src/js/mail_models/attachment_card.esm.js",
            "attachment_preview/static/src/js/mail_models/attachment_list.esm.js",
            "attachment_preview/static/src/js/web_views/binary_field.esm.js",
            "attachment_preview/static/src/js/web_views/form_renderer.esm.js",
            "attachment_preview/static/src/scss/attachment_preview.scss",
            "attachment_preview/static/src/xml/attachment_preview.xml",
        ],
        "web.assets_frontend": [],
        "web.assets_tests": [],
        "web.qunit_suite_tests": [],
    },
    "installable": True,
}
