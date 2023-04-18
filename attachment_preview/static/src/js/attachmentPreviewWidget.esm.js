/** @odoo-module */
import Widget from "web.Widget";

var active_attachment_index = 0;
var is_first_click = true;

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
        // First_click = true;
        var res = this._super.apply(this, arguments);
        this.$overlay = $(".attachment_preview_overlay");
        this.$iframe = $(".attachment_preview_iframe");
        this.$current = $(".attachment_preview_current");
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
        if (is_first_click) {
            is_first_click = !is_first_click;
        }
        var index = this.activeIndex + 1;
        if (index >= this.attachments.length) {
            index = 0;
        }
        this.activeIndex = index;
        this.updatePaginator();
        this.loadPreview();
    },

    previous: function () {
        if (is_first_click) {
            is_first_click = !is_first_click;
        }
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
        is_first_click = true;
        this.$el.addClass("d-none");
        this.trigger("hidden");
    },

    updatePaginator: function () {
        var value = _.str.sprintf(
            "%s / %s",
            this.activeIndex + 1,
            this.attachments.length
        );
        this.$overlay = $(".attachment_preview_overlay");
        this.$iframe = $(".attachment_preview_iframe");
        this.$current = $(".attachment_preview_current");
        this.$current.html(value);
    },

    loadPreview: function () {
        if (this.attachments.length === 0) {
            this.$iframe.attr("src", "about:blank");
            return;
        }

        if (is_first_click) {
            for (let i = 0; i < this.attachments.length; i++) {
                if (
                    parseInt(this.attachments[i].id, 10) === this.active_attachment_id
                ) {
                    active_attachment_index = i;
                    is_first_click = false;
                }
            }
        } else {
            active_attachment_index = this.activeIndex;
        }

        var att = this.attachments[active_attachment_index];
        this.$iframe.attr("src", att.previewUrl);
    },

    setAttachments: function (attachments, active_attachment_id, first_click) {
        is_first_click = first_click;

        if (active_attachment_id) {
            this.active_attachment_id = active_attachment_id;
        }
        if (attachments) {
            this.attachments = attachments;
            this.activeIndex = 0;
            this.updatePaginator();
            this.loadPreview();
        }
    },
});

export default AttachmentPreviewWidget;
