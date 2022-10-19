# Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class DocumentKnowledgeConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    module_attachment_indexation = fields.Boolean(
        "Attachments List and Document Indexation",
        help="Document indexation, full text search of attachements.\n"
        "- This installs the module attachment_indexation.",
    )

    group_ir_attachment_user = fields.Boolean(
        string="Central access to Documents",
        help="When you set this field all users will be able to manage "
        "attachments centrally, from the Document Knowledge/Documents menu.",
        implied_group="document_knowledge.group_ir_attachment_user",
    )

    module_document_page = fields.Boolean(
        "Manage document pages (Wiki)",
        help="Provide document page and category as a wiki.\n"
        "- This installs the module document_page.",
    )

    module_document_page_approval = fields.Boolean(
        "Manage documents approval",
        help="Add workflow on documents per category.\n"
        "- This installs the module document_page_approval.",
    )
