# Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class KnowledgeConfigSettings(models.TransientModel):

    _inherit = 'res.config.settings'

    module_document = fields.Boolean(
        'Manage documents',
        help='Document indexation, full text search of attachements.\n'
        '- This installs the module document.'
    )

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

    def get_values(self):
        res = super(KnowledgeConfigSettings, self).get_values()
        get_param = self.env['ir.config_parameter'].sudo().get_param
        res.update(
            module_document=get_param(
                'knowledge.module_document'),
            module_document_page=get_param(
                'knowledge.module_document_page'),
            module_document_page_approval=get_param(
                'knowledge.module_document_page_approval'),
            module_cmis_read=get_param(
                'knowledge.module_cmis_read'),
            module_cmis_write=get_param(
                'knowledge.module_cmis_write'),
        )
        return res

    def set_values(self):
        super(KnowledgeConfigSettings, self).set_values()
        set_param = self.env['ir.config_parameter'].sudo().set_param
        set_param('knowledge.module_document',
                  self.module_document)
        set_param('knowledge.module_document_page',
                  self.module_document_page)
        set_param('knowledge.module_document_page_approval',
                  self.module_document_page_approval)
        set_param('knowledge.module_cmis_read',
                  self.module_cmis_read)
        set_param('knowledge.module_cmis_write',
                  self.module_cmis_write)
