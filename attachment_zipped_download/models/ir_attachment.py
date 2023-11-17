# -*- coding: utf-8 -*-
# Copyright 2019 César Fernández Domínguez <cesfernandez@outlook.com>
# Copyright 2022 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
import base64
import zipfile
from io import BytesIO

from openerp import _, api, models
from openerp.exceptions import Warning as UserError


class IrAttachment(models.Model):
    _inherit = "ir.attachment"

    @api.multi
    def action_attachments_download(self):
        items = self.filtered(lambda x: x.type == "binary")
        if not items:
            raise UserError(
                _("None attachment selected. Only binary attachments allowed.")
            )
        item_names = [it._compute_zip_file_name() for it in items]
        if len(item_names) != len(set(item_names)):
            raise UserError(
                _("All file names must be unique.")
            )
        ids = ",".join(map(str, items.ids))
        return {
            "type": "ir.actions.act_url",
            "url": "/web/attachment/download_zip?ids=%s" % (ids),
            "target": "self",
        }

    @api.multi
    def _create_temp_zip(self):
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
            for attachment in self:
                attachment.check("read")
                zip_file.writestr(
                    attachment._compute_zip_file_name(),
                    base64.b64decode(attachment.datas),
                )
            zip_file.close()
        return zip_buffer

    @api.multi
    def _compute_zip_file_name(self):
        """Give a chance of easily changing the name of the file inside the ZIP."""
        self.ensure_one()
        return self.name
