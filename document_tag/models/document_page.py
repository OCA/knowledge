# Copyright (C) 2020 Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class DocumentPage(models.Model):
    _inherit = "document.page"

    tag_ids = fields.Many2many("document.tag", string="Tags")
