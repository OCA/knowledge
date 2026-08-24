# Copyright 2026 Jarsa
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Attachment Preview XML",
    "summary": "Preview XML attachments as a collapsible tree instead of raw text",
    "version": "17.0.1.0.0",
    "category": "Knowledge Management",
    "website": "https://github.com/OCA/knowledge",
    "author": "Jarsa, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": ["mail"],
    "assets": {
        "web.assets_backend": [
            "attachment_preview_xml/static/src/attachment_model_patch.esm.js",
            "attachment_preview_xml/static/src/xml_viewer.esm.js",
            "attachment_preview_xml/static/src/xml_viewer.xml",
            "attachment_preview_xml/static/src/xml_viewer.scss",
            "attachment_preview_xml/static/src/file_viewer_patch.esm.js",
            "attachment_preview_xml/static/src/file_viewer_patch.xml",
        ],
        "web.qunit_suite_tests": [
            "attachment_preview_xml/static/tests/**/*.js",
        ],
    },
    "installable": True,
}
