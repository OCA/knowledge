# Copyright 2020 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.fields import Domain


class IrAttachmentCategory(models.Model):
    _name = "ir.attachment.category"
    _description = "Attachment Category"
    _parent_store = True

    name = fields.Char()
    complete_name = fields.Char(
        compute="_compute_complete_name",
        store=True,
        recursive=True,
    )
    parent_id = fields.Many2one(
        "ir.attachment.category",
    )
    parent_path = fields.Char(
        index=True,
    )
    attachment_ids = fields.Many2many(
        compute="_compute_attachment_count", comodel_name="ir.attachment"
    )
    attachment_count = fields.Integer(
        compute="_compute_attachment_count",
    )

    @api.depends("name", "parent_id.complete_name")
    def _compute_complete_name(self):
        for category in self:
            if category.parent_id.complete_name:
                category.complete_name = (
                    f"{category.parent_id.complete_name}/{category.name}"
                )
            else:
                category.complete_name = category.name

    def _compute_display_name(self):
        for category in self:
            category.display_name = category.complete_name or category.name

    def _compute_attachment_count(self):
        category_obj = self.env["ir.attachment.category"]
        attachment_obj = self.env["ir.attachment"]
        for category in self:
            if not category.id:
                category.attachment_count = 0
                category.attachment_ids = attachment_obj.browse()
                continue
            child_categories = category_obj.search(
                Domain([("id", "child_of", category.id)])
            )
            attachment_ids = attachment_obj.search(
                Domain([("category_ids", "in", child_categories.ids)])
            )
            category.attachment_ids = attachment_ids
            category.attachment_count = len(attachment_ids)

    def action_attachment_view(self):
        self.ensure_one()
        action = self.env["ir.actions.act_window"]._for_xml_id("base.action_attachment")
        action["domain"] = Domain([("category_ids", "child_of", self.id)])
        context = self.env.context.copy()
        context.update({"default_category_ids": [self.id]})
        action["context"] = context
        return action
