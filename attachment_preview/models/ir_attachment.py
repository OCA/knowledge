# Copyright 2014 Therp BV (<http://therp.nl>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import collections
import logging
import mimetypes
import os.path

from odoo import api, models

_logger = logging.getLogger(__name__)


class IrAttachment(models.Model):
    _inherit = "ir.attachment"

    @api.model
    def get_binary_extension(self, model, ids, binary_field, filename_field=None):
        result = {}
        ids_to_browse = ids if isinstance(ids, collections.Iterable) else [ids]

        # First pass: load fields in bin_size mode to avoid loading big files
        #  unnecessarily.
        if filename_field:
            for this in (
                self.env[model].with_context(bin_size=True).browse(ids_to_browse)
            ):
                result[this.id] = False
                extension = ""
                if this[filename_field]:
                    filename, extension = os.path.splitext(this[filename_field])
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
            if not this[binary_field]:
                continue
            try:
                import magic

                if model == self._name and binary_field == "datas" and this.store_fname:
                    mimetype = magic.from_file(
                        this._full_path(this.store_fname), mime=True
                    )
                    _logger.debug(
                        "Magic determined mimetype %s from file %s",
                        mimetype,
                        this.store_fname,
                    )
                else:
                    mimetype = magic.from_buffer(this[binary_field], mime=True)
                    _logger.debug("Magic determined mimetype %s from buffer", mimetype)
            except ImportError:
                (mimetype, encoding) = mimetypes.guess_type(
                    "data:;base64," + this[binary_field].decode("utf-8"), strict=False
                )
                _logger.debug("Mimetypes guessed type %s from buffer", mimetype)
            extension = mimetypes.guess_extension(mimetype.split(";")[0], strict=False)
            result[this.id] = extension
        for _id in result:
            result[_id] = (result[_id] or "").lstrip(".").lower()
        return result if isinstance(ids, collections.Iterable) else result[ids]

    @api.model
    def get_attachment_extension(self, ids):
        return self.get_binary_extension(self._name, ids, "datas", "name")
