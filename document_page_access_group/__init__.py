# Copyright 2022 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from . import models


def uninstall_hook(env):
    """Enable again the permissions of document_page disabled by this module."""
    for xmlid in (
        "document_page.document_page_user",
        "document_page.document_page_editor",
    ):
        if access := env.ref(xmlid, raise_if_not_found=False):
            access.active = True
