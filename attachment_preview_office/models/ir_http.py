# Copyright 2026 Jarsa
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import shutil

from odoo import models


class IrHttp(models.AbstractModel):
    _inherit = "ir.http"

    def session_info(self):
        # Let the web client know whether office preview can work at all, so
        # the preview button is simply not shown on servers without LibreOffice
        # instead of opening a viewer that errors out with HTTP 503.
        info = super().session_info()
        info[
            "attachment_preview_office_available"
        ] = self._attachment_preview_office_available()
        return info

    @staticmethod
    def _attachment_preview_office_available():
        return bool(shutil.which("libreoffice"))
