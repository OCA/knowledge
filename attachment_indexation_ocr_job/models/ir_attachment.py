# Copyright 2023 len-foss/Financial Way
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, models

from odoo.addons.attachment_indexation_ocr.models.ir_attachment import _MARKER_PHRASE


class IrAttachment(models.Model):
    _inherit = "ir.attachment"

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for record in records:
            if record.index_content == _MARKER_PHRASE:
                desc = _("Perform OCR on attachment %s") % record.name
                record.with_delay(description=desc, channel="ocr").perform_ocr()
        return records
