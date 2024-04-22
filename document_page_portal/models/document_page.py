# Copyright 2020 - TODAY, Marcel Savegnago - Escodoo
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class DocumentPage(models.Model):

    _inherit = "document.page"

    is_public = fields.Boolean(
        "Public Page",
        help="If true it allows any user of the portal to have "
        "access to this document.",
    )
