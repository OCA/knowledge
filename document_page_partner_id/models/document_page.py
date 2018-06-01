# -*- coding: utf-8 -*-
# Copyright 2018 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class DocumentPage(models.Model):
    _inherit = 'document.page'

    partner_id = fields.Many2one('res.partner', 'Partner', index=True)
