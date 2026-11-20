# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import SUPERUSER_ID, api


def migrate(cr, version):
    """Disable the unrestricted permissions of document_page on upgrade.

    security/security.xml disables them in a noupdate block, which is only
    applied on install. When upgrading from 19.0, document_page creates these
    ir.access records active before this module is updated, so the noupdate
    block is skipped and every document user could read all pages.
    """
    env = api.Environment(cr, SUPERUSER_ID, {})
    for xmlid in (
        "document_page.document_page_user",
        "document_page.document_page_editor",
    ):
        if access := env.ref(xmlid, raise_if_not_found=False):
            access.active = False
