/** @odoo-module **/
import {
    registerClassPatchModel,
    registerInstancePatchModel,
    registerFieldPatchModel,
} from "@mail/model/model_core";

import {attr} from "@mail/model/model_field";

import FormRenderer from "web.FormRenderer";

import AttachmentPreviewWidget from "../../attachmentPreviewWidget";

var rpc = require("web.rpc");
var basic_fields = require("web.basic_fields");

var chatterpreviewableAttachments = [];
var active_attachment_id = 0;
var active_attachment_index = 0;
var first_click = true;

FormRenderer.include({
    custom_events: _.extend({}, FormRenderer.prototype.custom_events, {
        onAttachmentPreview: "_onAttachmentPreview",
    }),
    attachmentPreviewWidget: null,

    init: function (parent, state, params) {
        var res = this._super(...arguments);
        this.attachmentPreviewWidget = new AttachmentPreviewWidget(this);
        this.attachmentPreviewWidget.on(
            "hidden",
            this,
            this._attachmentPreviewWidgetHidden
        );
        return res;
    },

    start: function () {
        var self = this;
        return this._super.apply(this, arguments).then(function () {
            self.attachmentPreviewWidget.insertAfter(self.$el);
        });
    },

    _attachmentPreviewWidgetHidden: function () {
        this.$el.removeClass("attachment_preview");
    },

    showAttachmentPreviewWidget: function (first_click) {
        this.$el.addClass("attachment_preview");

        this.attachmentPreviewWidget.setAttachments(
            chatterpreviewableAttachments,
            active_attachment_id,
            first_click
        );
        this.attachmentPreviewWidget.show();
    },

    on_detach_callback: function () {
        this.attachmentPreviewWidget.hide();
        return this._super.apply(this, arguments);
    },

    _onAttachmentPreview: function () {
        first_click = true;
        this.showAttachmentPreviewWidget(first_click);
    },
});

function canPreview(extension) {
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
            "/web/content/" +
            attachment_id +
            "?model%3Dir.attachment";

        return url;
    }
}

registerInstancePatchModel(
    "mail.attachment_card",
    "attachment_preview/static/src/js/models/attachment_card/attachment_card.js",
    {
        /**
         * @override
         */
        _created() {
            this._super();
            this._onPreviewAttachment = this._onPreviewAttachment.bind(this);

            var attachments = _.object(
                this.attachmentList.attachments.map((attachment) => {
                    console.log("attachment", attachment);
                    return attachment.id;
                }),
                this.attachmentList.attachments.map((attachment) => {
                    if (
                        attachment.defaultSource &&
                        attachment.defaultSource.length > 38
                    ) {
                        return {
                            url: attachment.defaultSource,
                            extension: attachment.extension,
                            title: attachment.name,
                        };
                    } else {
                        return {
                            url: "/web/content?id=" + attachment.id + "&download=true",
                            extension: attachment.extension,
                            title: attachment.name,
                        };
                    }
                })
            );

            rpc.query({
                model: "ir.attachment",
                method: "get_attachment_extension",
                args: [
                    _.map(_.keys(attachments), function (id) {
                        return parseInt(id, 10);
                    }),
                ],
            }).then(function (extensions) {
                var reviewableAttachments = _.map(
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
                chatterpreviewableAttachments = reviewableAttachments;
            });
        },

        /**
         * @private
         */
        _showPreview(
            attachment_id,
            attachment_url,
            attachment_extension,
            attachment_title,
            split_screen
        ) {
            let active_attURL = "";
            this.attachmentList.attachments.forEach((att) => {
                if (parseInt(att.localId.slice(20).slice(0, -1)) === attachment_id) {
                    if (att.__values.url === undefined) {
                        att.__values.url = attachment_url.slice(
                            window.location.origin.length
                        );
                        active_attURL = att.__values.url;
                    }
                }
            });
            var url = getUrl(
                attachment_id,
                attachment_url,
                attachment_extension,
                attachment_title
            );

            console.log("active_attachment_id in _showPreview", active_attachment_id);
            console.log("url in _showPreview", url);
            if (split_screen) {
                this.component.trigger("onAttachmentPreview", {
                    url: url,
                    active_attachment_id: active_attachment_id,
                });
            } else {
                window.open(url);
            }
        },

        /**
         * @private
         */
        _onPreviewAttachment(event) {
            event.preventDefault();

            var self = this,
                $target = $(event.currentTarget),
                split_screen = $target.attr("data-target") !== "new",
                attachment_id = this.attachment.id,
                attachment_extension = "pdf",
                attachment_title = this.attachment.filename,
                attachment_url = this.attachment.defaultSource;
            active_attachment_id = attachment_id;

            if (attachment_extension) {
                this._showPreview(
                    attachment_id,
                    attachment_url,
                    attachment_extension,
                    attachment_title,
                    split_screen
                );
            } else {
                rpc.query({
                    model: "ir.attachment",
                    method: "get_attachment_extension",
                    args: [attachment_id],
                }).then(function (extension) {
                    this.showPreview(
                        attachment_id,
                        attachment_url,
                        extension,
                        null,
                        split_screen
                    );
                });
            }
        },
    }
);
