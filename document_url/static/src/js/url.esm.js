import {AttachmentList} from "@mail/core/common/attachment_list";
import {Chatter} from "@mail/chatter/web_portal_project/chatter";
import {patch} from "@web/core/utils/patch";
import {useService} from "@web/core/utils/hooks";

patch(Chatter.prototype, {
    setup() {
        super.setup();
        this.action = useService("action");
    },
    _onAddUrl() {
        this.action.doAction("document_url.action_ir_attachment_add_url", {
            additionalContext: {
                active_id: this.state.thread.id,
                active_ids: [this.state.thread.id],
                active_model: this.state.thread.model,
            },
            onClose: async () => {
                await this.updateThreadAttachments();
            },
        });
    },
    async updateThreadAttachments() {
        const attachments = await this.orm.call("ir.attachment", "search_read", [
            [
                ["res_model", "=", this.state.thread.model],
                ["res_id", "=", this.state.thread.id],
            ],
            ["id", "name", "mimetype", "url"],
        ]);
        this.state.thread.attachments = attachments.map((att) => ({
            id: att.id,
            name: att.name,
            mimetype: att.mimetype,
            url: att.url,
        }));
    },
    onClickAddAttachments(ev) {
        if (this.attachments.length) {
            return super.onClickAddAttachments(...arguments);
        }
        ev.stopPropagation();
        this.closeSearch();
        this.discardAttachmentSelection();
        this.state.activePanel =
            this.state.activePanel === this.CHATTER_PANEL.ATTACHMENT
                ? this.CHATTER_PANEL.NONE
                : this.CHATTER_PANEL.ATTACHMENT;
    },
});

patch(AttachmentList.prototype, {
    canDownload(attachment) {
        return (
            super.canDownload(attachment) && attachment.mimetype !== "application/link"
        );
    },
});
