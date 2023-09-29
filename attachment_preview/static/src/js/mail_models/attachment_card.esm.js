/** @odoo-module **/
import {query} from "web.rpc";
import {registerPatch} from "@mail/model/model_core";
import {showPreview} from "../utils.esm";

registerPatch({
    name: "AttachmentCard",
    recordMethods: {
        /**
         * @private
         * @param {event} event
         */
        _onPreviewAttachment(event) {
            event.preventDefault();

            var self = this,
                $target = $(event.currentTarget),
                split_screen = $target.attr("data-target") !== "new",
                attachment_id = this.attachment.id;

            query({
                model: "ir.attachment",
                method: "get_attachment_extension",
                args: [attachment_id],
            }).then(function (extension) {
                showPreview(
                    attachment_id,
                    self.attachment.defaultSource,
                    extension,
                    self.attachment.filename,
                    split_screen,
                    self.attachmentList.previewableAttachments
                );
            });
        },
    },
});
