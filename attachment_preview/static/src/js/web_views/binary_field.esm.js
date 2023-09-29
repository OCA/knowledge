/** @odoo-module **/
import {canPreview, showPreview} from "../utils.esm";
import {BinaryField} from "@web/views/fields/binary/binary_field";
import {_t} from "@web/core/l10n/translation";
import {onMounted} from "@odoo/owl";
import {patch} from "@web/core/utils/patch";
import {query} from "web.rpc";
import {sprintf} from "@web/core/utils/strings";

patch(BinaryField.prototype, "attachment_preview.BinaryField", {
    setup() {
        var res = this._super(...arguments);
        onMounted(this._preview_onMounted);
        return res;
    },

    _preview_onMounted() {
        if (this.props.record.data.id) {
            var self = this;
            query({
                model: "ir.attachment",
                method: "get_attachment_extension",
                args: [this.props.record.data.id],
            }).then(function (extension) {
                if (canPreview(extension)) {
                    self._renderPreviewButton(extension);
                }
            });
        }
    },

    _renderPreviewButton(extension) {
        // Add a button same as standard fa-download one.
        var dl_button = $(this.__owl__.bdom.parentEl).find("button.fa-download");
        if (dl_button.length !== 1) return;
        var preview_button = $("<button/>");
        preview_button.addClass("btn btn-secondary fa fa-external-link");
        preview_button.attr("data-tooltip", "Preview");
        preview_button.attr("aria-label", "Preview");
        preview_button.attr("title");
        preview_button.attr("data-extension", extension);
        dl_button.after(preview_button);
        preview_button.on("click", this._onPreview.bind(this));
    },

    _onPreview(event) {
        showPreview(
            null,
            sprintf(
                "/web/content?model=%s&field=%s&id=%s",
                this.props.record.resModel,
                this.props.name,
                this.props.record.data.id
            ),
            $(event.currentTarget).attr("data-extension"),
            sprintf(_t("Preview %s"), this.state.fileName),
            false,
            null
        );
        event.stopPropagation();
    },
});
