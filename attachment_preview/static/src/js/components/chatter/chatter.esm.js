/** @odoo-module **/
import AttachmentPreviewWidget from "../../attachmentPreviewWidget";
import {Chatter} from "@mail/components/chatter/chatter";
import {patch} from "web.utils";

odoo.define("attachment_preview.chatter", function (require) {
    const components = {Chatter};
    var rpc = require("web.rpc");
    var basic_fields = require("web.basic_fields");
    var core = require("web.core");
    var _t = core._t;

    function getUrl(
        attachment_id,
        attachment_url,
        attachment_extension,
        attachment_title
    ) {
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
                    "&zoom=automatic" +
                    "&title=" +
                    encodeURIComponent(attachment_title) +
                    "#" +
                    attachment_url.replace(window.location.origin, "");
            }
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
        }

        return url;
    }

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

    patch(
        components.Chatter.prototype,
        "attachment_preview/static/src/js/components/chatter/chatter.js",
        {
            /**
             * @override
             */
            constructor(...args) {
                this._super(...args);

                this._showPreview = this._showPreview.bind(this);
                this.canPreview = this.canPreview.bind(this);
            },

            /**
             * @override
             */
            _update() {
                // Var res = this._super.apply(this, arguments);
                var self = this;
                self._getPreviewableAttachments().then(function (atts) {
                    self.previewableAttachments = atts;
                    self._updatePreviewButtons(self.previewableAttachments);
                    if (!self.attachmentPreviewWidget) {
                        self.attachmentPreviewWidget = new AttachmentPreviewWidget(
                            self
                        );
                        self.attachmentPreviewWidget.setAttachments(atts);
                    }
                    self.previewableAttachments = atts;
                    // ChatterpreviewableAttachments = atts;
                    self.attachmentPreviewWidget.setAttachments(atts);
                });
            },

            _getPreviewableAttachments: function () {
                var self = this;
                var deferred = $.Deferred();
                const chatter = self.messaging.models["mail.chatter"].get(
                    self.props.chatterLocalId
                );
                const thread = chatter ? chatter.thread : undefined;

                var attachments = {};
                if (thread) {
                    attachments = thread.allAttachments;
                }

                attachments = _.object(
                    attachments.map((attachment) => {
                        return attachment.id;
                    }),
                    attachments.map((attachment) => {
                        if (attachment.defaultSource) {
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

                rpc.query({
                    model: "ir.attachment",
                    method: "get_attachment_extension",
                    args: [
                        _.map(_.keys(attachments), function (id) {
                            return parseInt(id, 10);
                        }),
                    ],
                }).then(
                    function (extensions) {
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

                        deferred.resolve(reviewableAttachments);
                    },

                    function () {
                        deferred.reject();
                    }
                );

                return deferred.promise();
            },

            _updatePreviewButtons: function (previewableAttachments) {
                $(this)
                    .find(".o_attachment_preview")
                    .each(function () {
                        var $this = $(this);
                        var att = _.findWhere(previewableAttachments, {
                            id: $this.attr("data-id"),
                        });
                        if (att) {
                            $this.attr("data-extension", att.extension);
                        } else {
                            $this.remove();
                        }
                    });
            },
        }
    );

    basic_fields.FieldBinaryFile.include(components.Chatter);
    basic_fields.FieldBinaryFile.include({
        showPreview(
            attachment_id,
            attachment_url,
            attachment_extension,
            attachment_title,
            split_screen
        ) {
            if (!canPreview(attachment_extension)) {
                return;
            }

            var url = getUrl(
                attachment_id,
                attachment_url,
                attachment_extension,
                attachment_title
            );

            if (split_screen) {
                this.trigger("onAttachmentPreview", {url: url});
            } else {
                window.open(url);
            }
        },

        _renderReadonly: function () {
            var self = this;
            this._super.apply(this, arguments);

            if (this.recordData.id) {
                this._getBinaryExtension().then(function (extension) {
                    if (canPreview(extension)) {
                        // Self._renderPreviewButton(extension, recordData);
                        self._renderPreviewButton(extension);
                    }
                });
            }
        },

        _renderPreviewButton: function (extension) {
            this.$previewBtn = $("<a/>");
            this.$previewBtn.addClass("fa fa-external-link mr-2");
            this.$previewBtn.attr("href");
            this.$previewBtn.attr(
                "title",
                _.str.sprintf(_t("Preview %s"), this.field.string)
            );
            this.$previewBtn.attr("data-extension", extension);
            this.$el.find(".fa-download").after(this.$previewBtn);
            this.$previewBtn.on("click", this._onPreview.bind(this));
        },

        _getBinaryExtension: function () {
            return rpc.query({
                model: "ir.attachment",
                method: "get_binary_extension",
                args: [this.model, this.recordData.id, this.name, this.attrs.filename],
            });
        },

        _onPreview: function (event) {
            this.showPreview(
                null,
                _.str.sprintf(
                    "/web/content?model=%s&field=%s&id=%d",
                    this.model,
                    this.name,
                    this.recordData.id
                ),
                $(event.currentTarget).attr("data-extension"),
                _.str.sprintf(_t("Preview %s"), this.field.string),
                false
            );
            event.stopPropagation();
        },
    });
});
