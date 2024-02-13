/** @odoo-module **/

import {registerPatch} from "@mail/model/model_core";
import {AttachmentCard} from "@mail/components/attachment_card/attachment_card";
import {patch} from "web.utils";
import {url} from "@web/core/utils/urls";

registerPatch({
    name: "AttachmentBoxView",
    recordMethods: {
        _onAddUrl(event) {
            event.preventDefault();
            event.stopPropagation();
            this.env.services.action.doAction(
                "document_url.action_ir_attachment_add_url",
                {
                    additionalContext: {
                        active_id: this.chatter.thread.id,
                        active_ids: [this.chatter.thread.id],
                        active_model: this.chatter.thread.model,
                    },
                    onClose: this._onAddedUrl.bind(this),
                }
            );
        },
        _onAddedUrl() {
            this.chatter.refresh();
        },
    },
});

registerPatch({
    name: "Chatter",
    recordMethods: {
        /**
         * Handles click on the attach button.
         */
        async onClickButtonAddAttachments() {
            await this.onClickButtonToggleAttachments();
        },
    },
});

patch(AttachmentCard.prototype, "document_url/static/src/js/url.js", {
    /**
     * Return the url of the attachment. Temporary attachments, a.k.a. uploading
     * attachments, do not have an url.
     *
     * @returns {String}
     */
    get attachmentUrl() {
        return url("/web/content", {
            id: this.attachmentCard.attachment.id,
            download: true,
        });
    },
});
