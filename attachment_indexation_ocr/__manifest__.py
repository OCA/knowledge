# © 2016 Therp BV <http://therp.nl>
# Copyright 2023 len-foss/Financial Way
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "OCR for documents",
    "version": "16.0.1.0.0",
    "author": "Therp BV,Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "website": "https://github.com/OCA/knowledge",
    "category": "Knowledge Management",
    "summary": "Run character recognition on uploaded files",
    "depends": ["attachment_indexation"],
    "data": [
        "data/ir_cron.xml",
        "data/ir_config_parameter.xml",
    ],
    "external_dependencies": {"bin": ["tesseract"], "python": ["PyMuPDF"]},
}
