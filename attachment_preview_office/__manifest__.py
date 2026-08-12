# Copyright 2026 Jarsa
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Attachment Preview Office",
    "summary": "Preview Office attachments in the browser "
    "by converting them to PDF with LibreOffice",
    "version": "17.0.1.0.0",
    "category": "Knowledge Management",
    "website": "https://github.com/OCA/knowledge",
    "author": "Jarsa, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": ["mail"],
    "assets": {
        "web.assets_backend": [
            "attachment_preview_office/static/src/attachment_model_patch.esm.js",
            "attachment_preview_office/static/src/file_viewer_patch.esm.js",
            "attachment_preview_office/static/src/file_viewer_patch.xml",
        ],
    },
    "installable": True,
}
