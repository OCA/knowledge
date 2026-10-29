# Copyright 2026 NuoBiT Solutions SL - Eric Antones <eantones@nuobit.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, models


class DocumentPage(models.Model):
    _inherit = "document.page"

    @api.model
    def get_empty_list_help(self, help_message):
        return "%(active_model)s %(active_id)s %(active_ids)s" % self.env.context
