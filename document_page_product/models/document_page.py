# Copyright 2026 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class DocumentPage(models.Model):
    _inherit = "document.page"

    product_tmpl_ids = fields.Many2many(
        comodel_name="product.template",
        relation="document_page_product_rel",
        column1="page_id",
        column2="product_tmpl_id",
        string="Product Templates",
    )
    product_template_count = fields.Integer(compute="_compute_product_template_count")

    @api.depends("product_tmpl_ids")
    def _compute_product_template_count(self):
        for item in self:
            item.product_template_count = len(item.product_tmpl_ids)

    def action_product_templates(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id(
            "product.product_template_action"
        )
        action["domain"] = [("id", "in", self.product_tmpl_ids.ids)]
        action["context"] = {}
        return action
