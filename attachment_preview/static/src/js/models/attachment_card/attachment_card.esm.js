/** @odoo-module **/
import {onMounted, onWillUnmount} from "@odoo/owl";
import {AttachmentPreviewWidget} from "../../attachmentPreviewWidget.esm";
import {FormRenderer} from "@web/views/form/form_renderer";
import {bus} from "web.core";
import {patch} from "@web/core/utils/patch";
import {query} from "web.rpc";
import {registerPatch} from "@mail/model/model_core";

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
// FormRenderer patch

export function canPreview(extension) {
    return (
        $.inArray(extension, [
            "odt",
            "odp",
            "ods",
            "fodt",
            "pdf",
            "ott",
            "fodp",
            "otp",
            "fods",
            "ots",
        ]) > -1
    );
}

function getUrl(attachment_id, attachment_url, attachment_extension, attachment_title) {
    var url = "";
    if (attachment_url) {
        if (attachment_url.slice(0, 21) === "/web/static/lib/pdfjs") {
            url = (window.location.origin || "") + attachment_url;
        } else {
            url =
                (window.location.origin || "") +
                "/attachment_preview/static/lib/ViewerJS/index.html" +
                "?type=" +
                encodeURIComponent(attachment_extension) +
                "&title=" +
                encodeURIComponent(attachment_title) +
                "&zoom=automatic" +
                "#" +
                attachment_url.replace(window.location.origin, "");
        }
        return url;
    }
    url =
        (window.location.origin || "") +
        "/attachment_preview/static/lib/ViewerJS/index.html" +
        "?type=" +
        encodeURIComponent(attachment_extension) +
        "&title=" +
        encodeURIComponent(attachment_title) +
        "&zoom=automatic" +
        "#" +
        "/web/content/" +
        attachment_id +
        "?model%3Dir.attachment";

    return url;
}

export function showPreview(
    attachment_id,
    attachment_url,
    attachment_extension,
    attachment_title,
    split_screen,
    attachment_info_list
) {
    if (split_screen && attachment_info_list) {
        bus.trigger("open_attachment_preview", attachment_id, attachment_info_list);
    } else {
        window.open(
            getUrl(
                attachment_id,
                attachment_url,
                attachment_extension,
                attachment_title
            )
        );
    }
}

registerPatch({
    name: "AttachmentList",
    lifecycleHooks: {
        _created() {
            var attachments = _.object(
                this.attachments.map((attachment) => {
                    return attachment.id;
                }),
                this.attachments.map((attachment) => {
                    if (
                        attachment.defaultSource &&
                        attachment.defaultSource.length > 38
                    ) {
                        return {
                            url: attachment.defaultSource,
                            extension: attachment.extension,
                            title: attachment.name,
                        };
                    }
                    return {
                        url: "/web/content?id=" + attachment.id + "&download=true",
                        extension: attachment.extension,
                        title: attachment.name,
                    };
                })
            );

            var self = this;
            query({
                model: "ir.attachment",
                method: "get_attachment_extension",
                args: [
                    _.map(_.keys(attachments), function (id) {
                        return parseInt(id, 10);
                    }),
                ],
            }).then(function (extensions) {
                self.previewableAttachments = _.map(
                    _.keys(
                        _.pick(extensions, function (extension) {
                            return canPreview(extension);
                        })
                    ),
                    function (id) {
                        return {
                            id: id,
                            url: attachments[id].url,
                            extension: extensions[id],
                            title: attachments[id].title,
                            previewUrl: getUrl(
                                id,
                                attachments[id].url,
                                extensions[id],
                                attachments[id].title
                            ),
                        };
                    }
                );
            });
        },
    },
});
// AttachmentList patch

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
// AttachmentCard patch
