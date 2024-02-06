# Copyright (C) 2023 Cetmix OÜ
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from urllib import parse

from odoo import api, models


class AddUrlWizard(models.TransientModel):
    _inherit = "ir.attachment.add_url"

    @api.model
    def add_attachment_google_drive(self, url, name, active_model, active_ids):
        attachment_obj = self.env["ir.attachment"]
        url_parse = parse.urlparse(url)
        if not url_parse.scheme:
            url_parse = parse.urlparse("{}{}".format("http://", url))
        for active_id in active_ids:
            attachment = {
                "name": name,
                "type": "url",
                "url": url_parse.geturl(),
                "res_id": active_id,
                "res_model": active_model,
            }
            attachment_obj.create(attachment)
