/** @odoo-module **/
import {onMounted, onWillUnmount} from "@odoo/owl";
import {AttachmentPreviewWidget} from "../attachmentPreviewWidget.esm";
import {FormRenderer} from "@web/views/form/form_renderer";
import {bus} from "web.core";
import {patch} from "@web/core/utils/patch";

patch(FormRenderer.prototype, "attachment_preview.FormRenderer", {
    attachmentPreviewWidget: null,

    setup() {
        var res = this._super(...arguments);
        this.attachmentPreviewWidget = new AttachmentPreviewWidget(this);
        this.attachmentPreviewWidget.on(
            "hidden",
            this,
            this._attachmentPreviewWidgetHidden
        );
        onMounted(() => {
            this.attachmentPreviewWidget.insertAfter($(".o_form_view"));
            bus.on("open_attachment_preview", this, this._onAttachmentPreview);
        });
        onWillUnmount(() => {
            bus.off("open_attachment_preview", this, this._onAttachmentPreview);
            this.attachmentPreviewWidget.hide();
            this.attachmentPreviewWidget.destroy();
        });
        return res;
    },

    _attachmentPreviewWidgetHidden() {
        $(".o_form_view").removeClass("attachment_preview");
    },

    _onAttachmentPreview(attachment_id, attachment_info_list) {
        $(".o_form_view").addClass("attachment_preview");
        this.attachmentPreviewWidget.setAttachments(
            attachment_info_list,
            attachment_id
        );
        this.attachmentPreviewWidget.show();
    },
});
