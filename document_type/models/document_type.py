from odoo import fields, models


class DocumentType(models.Model):
    _name = 'document.type'
    _description = 'Document Type'

    name = fields.Char(required=True)
    ir_model_id = fields.Many2one('ir.model', string='Object')
    document_ids = fields.One2many(
        'ir.attachment', 'document_type_id', string='Documents')
    documents_count = fields.Integer(compute='_compute_documents_count')

    def _compute_documents_count(self):
        for record in self:
            record.documents_count = len(record.document_ids)


class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    document_type_id = fields.Many2one(
        'document.type', string='Document Type',
        domain='[("ir_model_id.model", "=", res_model)]')
