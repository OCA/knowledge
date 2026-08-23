# Copyright 2026 - TODAY, Cristiano Mafra Junior <cristiano.mafra@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Document Page Helpdesk",
    "summary": "This module links document pages to helpdesk tickets",
    "version": "18.0.1.0.0",
    "category": "Helpdesk",
    "author": "Escodoo, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/knowledge",
    "license": "AGPL-3",
    "depends": ["helpdesk_mgmt", "document_page"],
    "maintainers": ["CristianoMafraJunior"],
    "data": ["views/document_page_views.xml", "views/helpdesk_ticket_views.xml"],
    "installable": True,
}
