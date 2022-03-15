# Copyright 2019 César Fernández Domínguez <cesfernandez@outlook.com>
# Copyright 2022 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
import zipfile
from io import BytesIO

from odoo import _, models
from odoo.exceptions import UserError


class IrAttachment(models.Model):
    _inherit = "ir.attachment"

    def action_attachments_download(self):
        items = self.filtered(lambda x: x.type == "binary")
        if not items:
            raise UserError(
                _("None attachment selected. Only binary attachments allowed.")
            )
        ids = ",".join(map(str, items.ids))
        return {
            "type": "ir.actions.act_url",
            "url": "/web/attachment/download_zip?ids=%s" % (ids),
            "target": "self",
        }

    def _create_temp_zip(self):
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
            for attachment in self:
                zip_file.write(
                    attachment._full_path(attachment.store_fname), attachment.name
                )
            zip_buffer.seek(0)
            zip_file.close()
        return zip_buffer
