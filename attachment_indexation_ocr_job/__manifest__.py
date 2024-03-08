# Copyright 2023 len-foss/Financial Way
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "OCR Jobs",
    "version": "16.0.1.0.0",
    "author": "len-foss/Financial Way,Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "website": "https://github.com/OCA/knowledge",
    "category": "Knowledge Management",
    "summary": "Run OCR through jobs",
    "depends": ["attachment_indexation_ocr", "queue_job"],
    "data": ["data/ir_cron.xml", "data/queue_job_channel.xml"],
}
