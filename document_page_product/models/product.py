# Copyright 2026 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    document_page_ids = fields.Many2many(
        comodel_name="document.page",
        relation="document_page_product_rel",
        column1="product_tmpl_id",
        column2="page_id",
        string="Document Pages",
    )
    document_page_count = fields.Integer(compute="_compute_document_page_count")

    @api.depends("document_page_ids")
    def _compute_document_page_count(self):
        for rec in self:
            rec.document_page_count = len(rec.document_page_ids)


class ProductProduct(models.Model):
    _inherit = "product.product"

    document_page_count = fields.Integer(compute="_compute_document_page_count")

    @api.depends("product_tmpl_id.document_page_count")
    def _compute_document_page_count(self):
        for rec in self:
            rec.document_page_count = rec.product_tmpl_id.document_page_count

    def action_document_page_products(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id(
            "document_page_product.action_document_page_products"
        )
        action["domain"] = [
            ("type", "=", "content"),
            ("product_tmpl_ids", "in", self.product_tmpl_id.ids),
        ]
        action["context"] = {
            "default_type": "content",
            "default_product_tmpl_ids": self.product_tmpl_id.ids,
        }
        return action
