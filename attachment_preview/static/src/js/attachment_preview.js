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

odoo.define('attachment_preview', function (require) {
    "use strict";

    var core = require('web.core');
    var session = require('web.session');
    var Model = require('web.Model');
    var Sidebar = require('web.Sidebar');
    var ListView = require('web.ListView');

    var _t = core._t;

    function show_preview(attachment_id, attachment_url, attachment_extension, attachment_title) {
        var url = ((window.location.origin || '') +
            '/attachment_preview/static/lib/ViewerJS/index.html' +
            '?type=' + encodeURIComponent(attachment_extension) +
            '&title=' + encodeURIComponent(attachment_title) +
            '#' +
            attachment_url.replace(window.location.origin, ''));
        window.open(url);
    }

    function can_preview(extension) {
        return jQuery.inArray(
            extension,
            [
                'odt', 'odp', 'ods', 'fodt', 'pdf', 'ott', 'fodp', 'otp',
                'fods', 'ots'
            ]) > -1;
    }

    Sidebar.include({
        on_attachments_loaded: function(attachments) {
            this._super(attachments);

            this.$('.oe_sidebar_attachment_preview')
                .click(this.on_attachment_preview);
            this.update_preview_buttons();
           // return _super.apply(self, arguments);
        },

        on_attachment_preview: function(e){
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
                show_preview(
                    attachment_id, attachment_url, attachment_extension,
                    attachment_title);
            }
            else
            {
                (new Model('ir.attachment')).call(
                    'get_attachment_extension', [attachment_id], {})
                .then(function(extension)
                {
                    show_preview(
                        attachment_id, attachment_url, extension[0], attachment_title);
                });
            }
        },

        update_preview_buttons: function(){
            var self = this;
            return (new Model('ir.attachment')).call(
                'get_attachment_extension',
                [
                    this.$('span.oe_sidebar_attachment_preview')
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
                            'span.oe_sidebar_attachment_preview[data-id="'+
                             id + '"]');
                        if(can_preview(extension[0]))
                        {
                            $element.attr('data-extension', extension[0]);
                        }
                        else
                        {
                            $element.remove();
                        }
                    });
                });
        },
    });

    ListView.include(
    {
        reload_content:  function() {
            var deferred = this._super.apply(this, arguments),
            self = this;
            deferred.then(function()
            {
                var $elements = self.$('.oe_binary_preview');
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
                    show_preview(
                        attachment_id,
                        $target.siblings('a').attr('href'),
                        attachment_extension,
                        $target.attr('alt'));
                });
                return (new Model('ir.attachment')).call(
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
                            if(can_preview(extension[0]))
                            {
                                $element.attr('data-extension', extension[0]);
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

    var ColumnBinary = core.list_widget_registry.get('field.binary').include({
       _format: function (row_data, options)
        {
            var link = this._super.apply(this, arguments);
            link += (
                '<a class="oe_binary_preview" title="'+_.str.sprintf(_t('Preview %s'), this.string)+
                    '" alt="'+_.str.sprintf(_t('Preview %s'), this.string)+'"'+
                ' data-id="'+options.id+'" data-model="'+options.model+'"'+
                ' data-field="'+this.id+'" data-filename="'+(this.filename || '')+'"'+
                ' src="/web/static/src/img/icons/gtk-print-preview.png" ><i class="fa fa-search"/></a>');
            return link;
        }
    });

    var FieldBinaryFile = core.form_widget_registry.get('binary').include({
        render_value: function()
        {
            this._super();
            if(this.get("effective_readonly") && this.get('value'))
            {
                var self = this;
                (new Model('ir.attachment')).call(
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
                        var $element = self.$('.oe_binary_preview');
                        $element.unbind( "click" );
                       if(can_preview(extension[0]))
                        {
                            $element.click(function()
                            {
                                show_preview(
                                    null,

                                        ('data:application/'+extension[0]+';base64,'+
                                        extension[1]),
                                    extension[0],
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
               this.$('.oe_binary_preview').remove();
            }
        },
    });
});
