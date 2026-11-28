import {Component, proxy} from "@odoo/owl";
import {useBus} from "@web/core/utils/hooks";

export class AttachmentPreviewWidget extends Component {
    static template = "attachment_preview.AttachmentPreviewWidget";

    setup() {
        super.setup();
        this.state = proxy({attachments: [], activeIndex: 0, visible: false});
        useBus(
            this.env.bus,
            "open_attachment_preview",
            ({detail: {attachment_id, attachment_info_list}}) => {
                this.state.attachments = attachment_info_list;
                this.state.activeIndex = Math.max(
                    0,
                    attachment_info_list.findIndex((item) => item.id === attachment_id)
                );
                this.state.visible = attachment_info_list.length > 0;
            }
        );
        useBus(this.env.bus, "hide_attachment_preview", () => this._onCloseClick());
    }

    get currentAttachment() {
        return this.state.attachments[this.state.activeIndex];
    }

    _onCloseClick() {
        this.state.visible = false;
        this.state.attachments = [];
        this.state.activeIndex = 0;
    }

    _onPreviousClick() {
        const count = this.state.attachments.length;
        if (count) {
            this.state.activeIndex = (this.state.activeIndex + count - 1) % count;
        }
    }

    _onNextClick() {
        const count = this.state.attachments.length;
        if (count) {
            this.state.activeIndex = (this.state.activeIndex + 1) % count;
        }
    }

    _onPopoutClick() {
        if (this.currentAttachment) {
            window.open(this.currentAttachment.previewUrl);
        }
    }
}
