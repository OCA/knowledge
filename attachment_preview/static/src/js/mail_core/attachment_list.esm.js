import {canPreview, getUrl, showPreview} from "../utils.esm";
import {AttachmentList} from "@mail/core/common/attachment_list";
import {_t} from "@web/core/l10n/translation";
import {patch} from "@web/core/utils/patch";

patch(AttachmentList.prototype, {
    _onPreviewAttachment(attachment, newWindow = false) {
        const attachments = this.props.attachments
            .filter((item) => this._canPreviewAttachment(item))
            .map((item) => ({
                id: item.id,
                previewUrl: getUrl(
                    item.id,
                    item.defaultSource,
                    item.extension,
                    item.name
                ),
            }));
        showPreview(
            attachment.id,
            attachment.defaultSource,
            attachment.extension,
            attachment.name,
            Boolean(this.env.inChatter) && !newWindow,
            attachments,
            this.env.bus
        );
    },

    _canPreviewAttachment(attachment) {
        return !attachment.uploading && canPreview(attachment.extension);
    },

    // Mobile attachment actions use a dropdown instead of the desktop hover buttons.
    getActions(attachment) {
        const actions = super.getActions(...arguments);
        if (this._canPreviewAttachment(attachment)) {
            actions.push({
                label: _t("Preview"),
                icon: "fa fa-search",
                onSelect: () => this._onPreviewAttachment(attachment),
            });
            actions.push({
                label: _t("Open preview in a new tab"),
                icon: "fa fa-external-link",
                onSelect: () => this._onPreviewAttachment(attachment, true),
            });
        }
        return actions;
    },
});
