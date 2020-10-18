# Copyright 2020 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class IrAttachment(models.Model):

    _inherit = "ir.attachment"

    category_ids = fields.Many2many(
        comodel_name="ir.attachment.category",
        relation="ir_attachment_category_rel",
        column1="attachment_id",
        column2="category_id",
        ondelete="restrict",
        index=True,
    )
