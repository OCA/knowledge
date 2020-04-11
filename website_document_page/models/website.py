# Copyright (C) 2020 Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class Website(models.Model):
    _inherit = "website"

    wiki_id = fields.Many2one("document.page", string="Wiki Main Page")
