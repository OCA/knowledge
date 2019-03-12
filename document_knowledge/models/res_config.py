# Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class KnowledgeConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    module_document = fields.Boolean(
        'Attachments List and Document Indexation',
        help='Document indexation, full text search of attachements.\n'
        '- This installs the module document.'
    )

    group_ir_attachment_user = fields.Boolean(
        string='Central access to Documents',
        help="When you set this field all users will be able to manage "
             "attachments centrally, from the Knowledge/Documents menu.",
        implied_group='knowledge.group_ir_attachment_user')

    module_document_page = fields.Boolean(
        'Manage document pages (Wiki)',
        help='Provide document page and category as a wiki.\n'
             '- This installs the module document_page.'
    )

    module_document_page_approval = fields.Boolean(
        'Manage documents approval',
        help='Add workflow on documents per category.\n'
             '- This installs the module document_page_approval.'
    )

    module_cmis_read = fields.Boolean(
        'Attach files from an external DMS into Odoo',
        help='Connect Odoo with a CMIS compatible server to attach files\n'
             'to an Odoo record.\n'
             '- This installs the module cmis_read.'
    )

    module_cmis_write = fields.Boolean(
        'Store attachments in an external DMS instead of the Odoo Filestore',
        help='Connect Odoo with a CMIS compatible server to store files.\n'
             '- This installs the module cmis_write.'
    )
