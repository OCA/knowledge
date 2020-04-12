# Copyright (C) 2020 Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class DocumentTag(models.Model):
    _name = "document.tag"
    _description = "Document Tag"

    name = fields.Char(index=True)
    parent_id = fields.Many2one("document.tag", string="Parent")
    company_id = fields.Many2one("res.company", string="Company")
