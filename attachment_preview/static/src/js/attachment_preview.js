//-*- coding: utf-8 -*-
//############################################################################
//
//   OpenERP, Open Source Management Solution
//   This module copyright (C) 2014 Therp BV (<http://therp.nl>).
//
//   This program is free software: you can redistribute it and/or modify
//   it under the terms of the GNU Affero General Public License as
//   published by the Free Software Foundation, either version 3 of the
//   License, or (at your option) any later version.
//
//   This program is distributed in the hope that it will be useful,
//   but WITHOUT ANY WARRANTY; without even the implied warranty of
//   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//   GNU Affero General Public License for more details.
//
//   You should have received a copy of the GNU Affero General Public License
//   along with this program.  If not, see <http://www.gnu.org/licenses/>.
//
//############################################################################

openerp.attachment_preview = function(instance)
{
    var _t = instance.web._t;
    openerp.attachment_preview.show_preview = function(
            attachment_id, attachment_url, attachment_extension,
            attachment_title)
    {
        var url = (window.location.origin || '') +
            '/attachment_preview/static/lib/ViewerJS/index.html#' +
            attachment_url.replace(window.location.origin, '') +
            '&title=' + encodeURIComponent(attachment_title) +
            '&ext=.' + encodeURIComponent(attachment_extension);
        window.open(url);
    };
    openerp.attachment_preview.can_preview = function(extension)
    {
        return jQuery.inArray(
            extension,
            [
                'odt', 'odp', 'ods', 'fodt', 'pdf', 'ott', 'fodp', 'otp',
                'fods', 'ots'
            ]) > -1;
    };
    instance.web.Sidebar.include(
    {
        on_attachments_loaded: function(attachments)
        {
            var result = this._super.apply(this, arguments);    
            this.$el.find('.oe-sidebar-attachment-preview')
                .click(this.on_attachment_preview);
            this.update_preview_buttons();
            return result;
        },
        on_attachment_preview: function(e)
        {
            e.preventDefault();
            e.stopPropagation();
            var self = this,
                $target = jQuery(e.currentTarget),
                attachment_id = parseInt($target.attr('data-id')),
                attachment_url = $target.attr('data-url'),
                attachment_extension = $target.attr('data-extension'),
                attachment_title = $target.attr('data-original-title');
            if(attachment_extension)
            {
                openerp.attachment_preview.show_preview(
                    attachment_id, attachment_url, attachment_extension,
                    attachment_title);
            }
            else
            {
                (new instance.web.Model('ir.attachment')).call(
                    'get_attachment_extension', [attachment_id], {})
                .then(function(extension)
                {
                    openerp.attachment_preview.show_preview(
                        attachment_id, attachment_url, extension);
                });
            }
        },
        update_preview_buttons: function()
        {
            var self = this;
            return (new instance.web.Model('ir.attachment')).call(
                'get_attachment_extension',
                [
                    this.$el.find('.oe-sidebar-attachment-preview')
                    .map(function()
                    {
                        return parseInt(jQuery(this).attr('data-id'));
                    })
                    .get()
                ],
                {})
                .then(function(extensions)
                {
                    _(extensions).each(function(extension, id)
                    {
                        var $element = jQuery(
                            'a.oe-sidebar-attachment-preview[data-id="'
                            + id + '"]');
                        if(openerp.attachment_preview.can_preview(extension))
                        {
                            $element.attr('data-extension', extension);
                        }
                        else
                        {
                            $element.remove();
                        }
                    });
                });
        },
    });
    instance.web.ListView.include(
    {
        reload_content: function()
        {
            var deferred = this._super.apply(this, arguments),
                self = this;
            deferred.then(function()
            {
                var $elements = self.$el.find('.oe-binary-preview');
                if(!$elements.length)
                {
                    return;
                }
                $elements.click(function(e)
                {
                    e.stopPropagation();
                    var $target = jQuery(e.currentTarget),
                        attachment_id = parseInt($target.attr('data-id')),
                        attachment_extension = $target.attr('data-extension');
                    openerp.attachment_preview.show_preview(
                        attachment_id,
                        $target.siblings('a').attr('href'),
                        attachment_extension,
                        $target.attr('alt'));
                });
                return (new instance.web.Model('ir.attachment')).call(
                    'get_binary_extension',
                    [
                        $elements.attr('data-model'),
                        $elements
                        .map(function()
                        {
                            return parseInt(jQuery(this).attr('data-id'));
                        })
                        .get(),
                        $elements.attr('data-field'),
                        $elements.attr('data-filename'),
                    ],
                    {})
                    .then(function(extensions)
                    {
                        _(extensions).each(function(extension, id)
                        {
                            var $element = $elements.filter(
                                '[data-id="' + id + '"]');
                            if(openerp.attachment_preview.can_preview(extension))
                            {
                                $element.attr('data-extension', extension);
                            }
                            else
                            {
                                $element.remove();
                            }
                        });
                    });
            });
            return deferred;
        }
    });
    instance.web.list.Binary.include(
    {
        _format: function (row_data, options)
        {
            var link = this._super.apply(this, arguments);
            link += _.template(
                '<img class="oe-binary-preview" title="<%-preview_text%>" alt="<%-preview_text%>" data-id="<%-preview_id%>" data-model="<%-preview_model%>" data-field="<%-preview_field%>" data-filename="<%-preview_filename%>" src="/web/static/src/img/icons/gtk-print-preview.png" />',
                {
                    preview_id: options.id,
                    preview_text: _.str.sprintf(_t('Preview %s'), this.string),
                    preview_model: options.model,
                    preview_field: this.id,
                    preview_filename: this.filename || '',
                });
            return link;
        }
    });
    instance.web.form.FieldBinaryFile.include(
    {
        render_value: function()
        {
            this._super.apply(this, arguments);
            if(this.get("effective_readonly") && this.get('value'))
            {
                var self = this;
                (new instance.web.Model('ir.attachment')).call(
                    'get_binary_extension',                                                                    [
                    this.view.dataset.model,
                    this.view.datarecord.id ? [this.view.datarecord.id] : [],
                    this.name,
                    this.node.attrs.filename,
                    ],
                    {})
                .then(function(extensions)
                {
                    _(extensions).each(function(extension)
                    {
                        var $element = self.$el.find('.oe-binary-preview');
                        if(openerp.attachment_preview.can_preview(extension))
                        {
                            $element.click(function()
                            {
                                openerp.attachment_preview.show_preview(
                                    null,
                                    _.str.sprintf(
                                        '/web/binary/saveas?session_id=%s&model=%s&field=%s&id=%d',
                                        instance.session.session_id,
                                        self.view.dataset.model,
                                        self.name,
                                        self.view.datarecord.id),
                                    extension,
                                    _.str.sprintf(_t('Preview %s'), self.field.string));
                            });
                            $element.attr('title', _.str.sprintf(_t('Preview %s'), self.field.string));
                        }
                        else
                        {
                            $element.remove();
                        }
                    });
                });
            }
            else
            {
                this.$el.find('.oe-binary-preview').remove();
            };
        },
    });
}    
