/** @odoo-module **/

import {AttachmentBox} from "@mail/components/attachment_box/attachment_box";
import {AttachmentCard} from "@mail/components/attachment_card/attachment_card";
import {patch} from "web.utils";
import {url} from "@web/core/utils/urls";

patch(AttachmentBox.prototype, "document_url/static/src/js/url.js", {
    _onAddUrl(event) {
        event.preventDefault();
        event.stopPropagation();
        if (this.env.model) {
            this.env.services.action.doAction(
                "document_url.action_ir_attachment_add_url",
                {
                    additionalContext: {
                        active_id: this.env.model.root.data.id,
                        active_ids: [this.env.model.root.data.id],
                        active_model: this.env.model.root.resModel,
                    },
                    onClose: this._onAddedUrl.bind(this),
                }
            );
        }
    },
    _onAddedUrl() {
        this.props.record.chatter.refresh();
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
