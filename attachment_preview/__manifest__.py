# Copyright 2014 Therp BV (<http://therp.nl>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Preview attachments",
    "version": "18.0.1.0.1",
    "author": "Therp BV," "Onestein," "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/knowledge",
    "license": "AGPL-3",
    "summary": "Preview attachments (PDF + office) via the native PDF.js viewer",
    "category": "Knowledge Management",
    "depends": ["web", "mail"],
    # Office preview (DOCX/XLSX/PPTX + ODF) converts to PDF with LibreOffice
    # headless. Declared as a "deb" external dependency so OCA CI / runboat
    # apt-install it; on other deployments it degrades gracefully (HTTP 503)
    # when LibreOffice is absent, so PDF preview still works without it.
    "external_dependencies": {
        "deb": [
            "libreoffice-calc",
            "libreoffice-impress",
            "libreoffice-writer",
        ],
    },
    "data": [],
    "qweb": [],
    "assets": {
        "web._assets_primary_variables": [],
        "web.assets_backend": [
            "attachment_preview/static/src/js/attachmentPreviewWidget.esm.js",
            "attachment_preview/static/src/js/utils.esm.js",
            "attachment_preview/static/src/js/mail_core/attachment_list.esm.js",
            "attachment_preview/static/src/js/web_views/fields/binary_field.esm.js",
            "attachment_preview/static/src/js/web_views/form/form_compiler.esm.js",
            "attachment_preview/static/src/js/web_views/form/form_controller.esm.js",
            "attachment_preview/static/src/js/web_views/form/form_renderer.esm.js",
            "attachment_preview/static/src/scss/attachment_preview.scss",
            "attachment_preview/static/src/xml/attachment_preview.xml",
        ],
    },
    "installable": True,
}
