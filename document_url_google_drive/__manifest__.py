# Copyright (C) 2023 Cetmix OÜ
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    "name": "Google Drive URL attachment",
    "version": "16.0.1.0.0",
    "category": "Tools",
    "website": "https://github.com/OCA/knowledge",
    "author": "Cetmix, Odoo Community Association (OCA)",
    "maintainers": ["CetmixGitDrone"],
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "document_url",
        "google_account",
    ],
    "data": [
        "views/res_users_view.xml",
        "views/res_config_settings_view.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "document_url_google_drive/static/src/js/attachment_google_picker.esm.js",
            "document_url_google_drive/static/src/xml/google_picker_url.xml",
            "document_url_google_drive/static/src/xml/attachment_google_picker.xml",
            "document_url_google_drive/static/src/js/attachment_card.esm.js",
        ],
    },
}
