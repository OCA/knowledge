odoo.define("/attachment_preview/static/src/js/attachment_preview.js", function (
    require
) {
    "use strict";
    const components = {
        Attachment: require("mail/static/src/components/attachment/attachment.js"),
        Chatter: require("mail/static/src/components/chatter/chatter.js"),
        ChatterContainer: require("mail/static/src/components/chatter_container/chatter_container.js"),
    };
    const {patch} = require("web.utils");
    var rpc = require("web.rpc");
    var basic_fields = require("web.basic_fields");
    var FormRenderer = require("web.FormRenderer");
    var Widget = require("web.Widget");
    var core = require("web.core");
    var _t = core._t;

    const attachment = patch(
        components.Attachment,
        "mail/static/src/components/attachment/attachment.js",
        {
            events: _.extend({}, components.Chatter.prototype.events, {
                "click .o_attachment_preview": "_onPreviewAttachment",
            }),
            canPreview: function (extension) {
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
            },

            getUrl: function (
                attachment_id,
                attachment_url,
                attachment_extension,
                attachment_title
            ) {
                var url =
                    (window.location.origin || "") +
                    "/attachment_preview/static/lib/ViewerJS/index.html" +
                    "?type=" +
                    encodeURIComponent(attachment_extension) +
                    "&title=" +
                    encodeURIComponent(attachment_title) +
                    "#" +
                    attachment_url.replace(window.location.origin, "");
                return url;
            },

            showPreview(
                attachment_id,
                attachment_url,
                attachment_extension,
                attachment_title,
                split_screen
            ) {
                var url = this.getUrl(
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

            _onPreviewAttachment(event) {
                event.preventDefault();
                var self = this,
                    $target = $(event.currentTarget),
                    split_screen = $target.attr("data-target") !== "new",
                    attachment_id = parseInt($target.attr("data-id"), 10),
                    attachment_extension = "pdf",
                    attachment_title = $target.attr("data-original-title"),
                    attachment_url = this.attachmentUrl;
                if (attachment_extension) {
                    this.showPreview(
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
                        self.showPreview(
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

    var AttachmentPreviewWidget = Widget.extend({
        template: "attachment_preview.AttachmentPreviewWidget",
        activeIndex: 0,

        events: {
            "click .attachment_preview_close": "_onCloseClick",
            "click .attachment_preview_previous": "_onPreviousClick",
            "click .attachment_preview_next": "_onNextClick",
            "click .attachment_preview_popout": "_onPopoutClick",
        },

        start: function () {
            var res = this._super.apply(this, arguments);
            this.$overlay = this.$el.find(".attachment_preview_overlay");
            this.$iframe = this.$el.find(".attachment_preview_iframe");
            this.$current = this.$el.find(".attachment_preview_current");
            return res;
        },

        _onCloseClick: function () {
            this.hide();
        },

        _onPreviousClick: function () {
            this.previous();
        },

        _onNextClick: function () {
            this.next();
        },

        _onPopoutClick: function () {
            if (!this.attachments[this.activeIndex]) {
                return;
            }

            window.open(this.attachments[this.activeIndex].previewUrl);
        },

        next: function () {
            var index = this.activeIndex + 1;
            if (index >= this.attachments.length) {
                index = 0;
            }
            this.activeIndex = index;
            this.updatePaginator();
            this.loadPreview();
        },

        previous: function () {
            var index = this.activeIndex - 1;
            if (index < 0) {
                index = this.attachments.length - 1;
            }
            this.activeIndex = index;
            this.updatePaginator();
            this.loadPreview();
        },

        show: function () {
            this.$el.removeClass("d-none");
            this.trigger("shown");
        },

        hide: function () {
            this.$el.addClass("d-none");
            this.trigger("hidden");
        },

        updatePaginator: function () {
            var value = _.str.sprintf(
                "%s / %s",
                this.activeIndex + 1,
                this.attachments.length
            );
            this.$overlay = $(this).find(".attachment_preview_overlay");
            this.$iframe = $(this).find(".attachment_preview_iframe");
            this.$current = $(this).find(".attachment_preview_current");
            this.$current.html(value);
        },

        loadPreview: function () {
            if (this.attachments.length === 0) {
                this.$iframe.attr("src", "about:blank");
                return;
            }

            var att = this.attachments[this.activeIndex];
            this.$iframe.attr("src", att.previewUrl);
        },

        setAttachments: function (attachments) {
            if (attachments) {
                this.attachments = attachments;
                this.activeIndex = 0;
                this.updatePaginator();
                this.loadPreview();
            }
        },
    });

    const chatter = patch(
        components.Chatter,
        "mail/static/src/components/chatter/chatter.js",
        {
            canPreview: function (extension) {
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
            },

            getUrl: function (
                attachment_id,
                attachment_url,
                attachment_extension,
                attachment_title
            ) {
                return (
                    (window.location.origin || "") +
                    "/attachment_preview/static/lib/ViewerJS/index.html" +
                    "?type=" +
                    encodeURIComponent(attachment_extension) +
                    "&title=" +
                    encodeURIComponent(attachment_title) +
                    "#" +
                    attachment_url.replace(window.location.origin, "")
                );
            },

            showPreview(
                attachment_id,
                attachment_url,
                attachment_extension,
                attachment_title,
                split_screen
            ) {
                var url = this.getUrl(
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

            _update() {
                var self = this;
                self.getPreviewableAttachments().done(
                    function (atts) {
                        this.updatePreviewButtons(this.previewableAttachments);
                        if (!this.attachmentPreviewWidget) {
                            this.attachmentPreviewWidget = new AttachmentPreviewWidget(
                                this
                            );
                            this.attachmentPreviewWidget.setAttachments(atts);
                        }
                        this.props.previewableAttachments = atts;
                        this.attachmentPreviewWidget.setAttachments(atts);
                    }.bind(this)
                );
            },

            getPreviewableAttachments: function () {
                var self = this;
                var deferred = $.Deferred();
                var $items = $(".o_attachment_preview");
                var attachments = _.object(
                    $items.map(function () {
                        return parseInt($(this).attr("data-id"), 10);
                    }),
                    $items.map(function () {
                        return {
                            url: $(this).attr("data-url"),
                            extension: $(this).attr("data-extension"),
                            title: $(this).attr("data-original-title"),
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
                                    return self.canPreview(extension);
                                })
                            ),
                            function (id) {
                                return {
                                    id: id,
                                    url: attachments[id].url,
                                    extension: extensions[id],
                                    title: attachments[id].title,
                                    previewUrl: self.getUrl(
                                        id,
                                        attachments[id].url,
                                        extensions[id],
                                        id + " - " + attachments[id].title
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

            updatePreviewButtons: function (previewableAttachments) {
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
        events: _.extend({}, basic_fields.FieldBinaryFile.prototype.events, {
            "click .fa-search": "_onPreview",
        }),

        _renderReadonly: function () {
            var self = this;
            this._super.apply(this, arguments);

            if (this.recordData.id) {
                this._getBinaryExtension().done(function (extension) {
                    if (self.canPreview(extension)) {
                        self._renderPreviewButton(extension);
                    }
                });
            }
        },

        _renderPreviewButton: function (extension) {
            this.$previewBtn = $("<a/>");
            this.$previewBtn.addClass("fa fa-search mr-2");
            this.$previewBtn.attr("href");
            this.$previewBtn.attr(
                "title",
                _.str.sprintf(_t("Preview %s"), this.field.string)
            );
            this.$previewBtn.attr("data-extension", extension);
            this.$el.find(".fa-download").before(this.$previewBtn);
        },

        _getBinaryExtension: function () {
            return this._rpc({
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

    FormRenderer.include({
        custom_events: _.extend({}, FormRenderer.prototype.custom_events, {
            onAttachmentPreview: "_onAttachmentPreview",
        }),
        attachmentPreviewWidget: null,

        init: function () {
            var res = this._super.apply(this, arguments);
            this.attachmentPreviewWidget = new AttachmentPreviewWidget(this);
            this.attachmentPreviewWidget.on(
                "hidden",
                this,
                this._attachmentPreviewWidgetHidden
            );
            return res;
        },

        start: function () {
            this._super.apply(this, arguments);
            this.attachmentPreviewWidget.insertAfter(this.$el);
        },

        _attachmentPreviewWidgetHidden: function () {
            this.$el.removeClass("attachment_preview");
        },

        showAttachmentPreviewWidget: function () {
            this.$el.addClass("attachment_preview");
            this.attachmentPreviewWidget.setAttachments(this.previewableAttachments);
            this.attachmentPreviewWidget.show();
        },

        on_detach_callback: function () {
            this.attachmentPreviewWidget.hide();
            return this._super.apply(this, arguments);
        },

        _onAttachmentPreview: function () {
            this.showAttachmentPreviewWidget();
        },
    });

    return {
        attachment,
        chatter,
        AttachmentPreviewWidget: AttachmentPreviewWidget,
    };
});
