/** @odoo-module **/

import {AttachmentBox} from "@mail/components/attachment_box/attachment_box";
import {AttachmentCard} from "@mail/components/attachment_card/attachment_card";
import {patch} from "web.utils";

patch(AttachmentBox.prototype, "document_url/static/src/js/url.js", {
    _onAddUrl(event) {
        event.preventDefault();
        event.stopPropagation();
        this.env.bus.trigger("do-action", {
            action: "document_url.action_ir_attachment_add_url",
            options: {
                additional_context: {
                    active_id: this.messaging.models["mail.chatter"].get(
                        this.props.chatterLocalId
                    ).threadId,
                    active_ids: [
                        this.messaging.models["mail.chatter"].get(
                            this.props.chatterLocalId
                        ).threadId,
                    ],
                    active_model: this.messaging.models["mail.chatter"].get(
                        this.props.chatterLocalId
                    ).threadModel,
                },
                on_close: this._onAddedUrl.bind(this),
            },
        });
    },
    _onAddedUrl() {
        this.trigger("reload");
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
        return this.env.session.url("/web/content", {
            id: this.attachmentCard.attachment.id,
            download: true,
        });
    },
});
