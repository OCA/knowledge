///* Copyright 2014 Therp BV (<http://therp.nl>)
// * License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl). */

odoo.define('attachment_preview', function(require) {
    'use strict';

    var core = require('web.core');
    var _t = core._t;
    var Sidebar = require('web.Sidebar');
    var basic_fields = require('web.basic_fields');

    var AttachmentPreviewMixin = {
        canPreview: function(extension) {
            return $.inArray(
                extension,
                [
                    'odt', 'odp', 'ods', 'fodt', 'pdf', 'ott', 'fodp', 'otp',
                    'fods', 'ots'
                ]) > -1;
        },
        showPreview: function(attachment_id, attachment_url, attachment_extension, attachment_title) {
            var url = (window.location.origin || '') +
                '/attachment_preview/static/lib/ViewerJS/index.html' +
                '?type=' + encodeURIComponent(attachment_extension) +
                '&title=' + encodeURIComponent(attachment_title) +
                '#' +
                attachment_url.replace(window.location.origin, '');
            window.open(url);
        }
    };

    Sidebar.include(AttachmentPreviewMixin);
    Sidebar.include({
        _redraw: function () {
            this._super.apply(this, arguments);
            this.$('.o_sidebar_preview_attachment')
                .click(this._onPreviewAttachment.bind(this));
            this.updatePreviewButtons();
        },
        _onPreviewAttachment: function(event) {
            event.preventDefault();
            var self = this,
                $target = $(event.currentTarget),
                attachment_id = parseInt($target.attr('data-id'), 10),
                attachment_url = $target.attr('data-url'),
                attachment_extension = $target.attr('data-extension'),
                attachment_title = $target.attr('data-original-title');

            if(attachment_extension) {
                this.showPreview(attachment_id, attachment_url, attachment_extension, attachment_title);
            } else {
                this._rpc({
                    model: 'ir.attachment',
                    method: 'get_attachment_extension',
                    args: [attachment_id]
                }).then(function(extension) {
                    self.showPreview(attachment_id, attachment_url, extension);
                });
            }
        },
        updatePreviewButtons: function() {
            var self = this;
            return this._rpc({
                model: 'ir.attachment',
                method: 'get_attachment_extension',
                args: [
                    this.$el.find('.o_sidebar_preview_attachment').map(function() {
                        return parseInt($(this).attr('data-id'), 10);
                    }).get()
                ]
            }).then(function(extensions) {
                _(extensions).each(function(extension, id) {
                    var $element = self.$el.find('span.o_sidebar_preview_attachment[data-id="' + id + '"]');
                    if (self.canPreview(extension)) {
                        $element.attr('data-extension', extension);
                    } else {
                        $element.remove();
                    }
                });
            });
        },

    });

    basic_fields.FieldBinaryFile.include(AttachmentPreviewMixin);
    basic_fields.FieldBinaryFile.include({
        events: _.extend({}, basic_fields.FieldBinaryFile.prototype.events, {
            'click .fa-search': '_onPreview'
        }),
        _renderReadonly: function () {
            var self = this;
            this._super.apply(this, arguments);
            this._getBinaryExtension().done(function(extension) {
                if(self.canPreview(extension)) {
                    self._renderPreviewButton(extension);
                }
            });
        },
        _renderPreviewButton: function(extension) {
            this.$previewBtn = $("<span/>");
            this.$previewBtn.addClass('fa fa-search');
            this.$previewBtn.attr('title', _.str.sprintf(_t('Preview %s'), this.field.string));
            this.$previewBtn.attr('data-extension', extension);
            this.$el.find('.fa-download').after(this.$previewBtn);
        },
        _getBinaryExtension: function () {
            return this._rpc({
                model: 'ir.attachment',
                method: 'get_binary_extension',
                args: [
                    this.model,
                    this.recordData.id,
                    this.name,
                    this.attrs.filename
                ]
            });
        },
        _onPreview: function(event) {
            this.showPreview(
                null,
                _.str.sprintf(
                    '/web/content?model=%s&field=%s&id=%d',
                    this.model,
                    this.name,
                    this.recordData.id
                ),
                $(event.currentTarget).attr('data-extension'),
                _.str.sprintf(_t('Preview %s'), this.field.string)
            );
        }
    });

    return {
        AttachmentPreviewMixin: AttachmentPreviewMixin
    };
});
