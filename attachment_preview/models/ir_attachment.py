# Copyright 2014 Therp BV (<http://therp.nl>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import collections
import logging
import mimetypes
import os.path

from odoo import api, models

from odoo.addons.mail.tools.discuss import Store

_logger = logging.getLogger(__name__)


class IrAttachment(models.Model):
    _inherit = "ir.attachment"

    @api.model
    def get_binary_extension(self, model, ids, binary_field, filename_field=None):
        result = {}
        ids_to_browse = ids if isinstance(ids, collections.abc.Iterable) else [ids]

        # First pass: load fields in bin_size mode to avoid loading big files
        #  unnecessarily.
        if filename_field:
            for this in (
                self.env[model].with_context(bin_size=True).browse(ids_to_browse)
            ):
                extension = ""
                if hasattr(this, filename_field) and this[filename_field]:
                    extension = os.path.splitext(this[filename_field])[1]
                if this[binary_field] and extension:
                    result[this.id] = extension
                    _logger.debug(
                        "Got extension %s from filename %s",
                        extension,
                        this[filename_field],
                    )
        # Second pass for all attachments which have to be loaded fully
        #  to get the extension from the content
        ids_to_browse = [_id for _id in ids_to_browse if _id not in result]
        for this in self.env[model].with_context(bin_size=True).browse(ids_to_browse):
            result[this.id] = False
            mimetype = False
            try:
                import magic

                if (
                    model == self._name and binary_field == "raw" and this.store_fname
                ):  # pragma: no cover
                    mimetype = magic.from_file(
                        this._full_path(this.store_fname), mime=True
                    )
                else:  # pragma: no cover
                    mimetype = magic.from_buffer(bytes(this[binary_field]), mime=True)
                    _logger.debug("Magic determined mimetype %s from buffer", mimetype)
            except (ImportError, Exception):  # noqa: BLE001
                try:
                    # Binary fields hold a BinaryValue, which guesses its mimetype.
                    mimetype = this[binary_field].mimetype
                except Exception as e:  # noqa: BLE001
                    _logger.debug("Error when guessing mimetype: %s", str(e))
            if mimetype:
                extension = mimetypes.guess_extension(
                    mimetype.split(";")[0], strict=False
                )
                result[this.id] = extension
        for _id, extension in result.items():
            result[_id] = (extension or "").lstrip(".").lower()
        return result if isinstance(ids, collections.abc.Iterable) else result[ids]

    @api.model
    def get_attachment_extension(self, ids):
        return self.get_binary_extension(self._name, ids, "raw", "name")

    def _store_attachment_fields(self, res: Store.FieldList, **kwargs):
        """Adds extension to the attachment fields sent to the web client"""
        result = super()._store_attachment_fields(res, **kwargs)
        res.attr("extension", lambda a: a.get_attachment_extension(a.id))
        return result
