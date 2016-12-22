# -*- coding: utf-8 -*-
# Copyright 2016 MONK Software
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class KnowledgeConfigSettings(models.TransientModel):

    _name = 'knowledge.config.settings'
    _inherit = 'res.config.settings'

    module_document = fields.Boolean(
        'Manage documents',
        help='Document indexation, full text search of attachements.\n'
        '- This installs the module document.'
    )
