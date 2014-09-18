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
        attachment_id, attachment_url, attachment_extension, attachment_title)
    {
        var url = window.location.origin +
            '/attachment_preview/static/lib/ViewerJS/index.html#' +
            attachment_url.replace(window.location.origin, '') +
            '&title=' + encodeURIComponent(attachment_title || _t('Preview')) +
            '&ext=.' + encodeURIComponent(attachment_extension);
        window.open(url);
    };
    openerp.attachment_preview.can_preview = function(extension)
    {
        return jQuery.inArray(
            extension, ['odt', 'odp', 'ods', 'fodt', 'pdf']) > -1;
    },
    instance.web.form.SidebarAttachments.include(
    {
        init: function(parent, form_view)
        {
            this.attachment_title_preview = function(name)
            {
                return _.str.sprintf(
                    instance.web._t("Preview attachment %s"), name);
            };
            return this._super.apply(this, arguments);
        },
        on_attachments_loaded: function(attachments)
        {
            var result = this._super.apply(this, arguments);    
            this.$element.find('.oe-sidebar-attachment-preview')
                .click(this.on_attachment_preview);
            this.update_preview_buttons();
            return result;
        },
        on_attachment_preview: function(e)
        {
            var self = this,
                $target = jQuery(e.currentTarget),
                attachment_id = parseInt($target.attr('data-id')),
                attachment_url = $target.attr('data-url'),
                attachment_extension = $target.attr('data-extension'),
                attachment_title = $target.attr('title');
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
                    this.$element.find('.oe-sidebar-attachment-preview')
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
    instance.web.page.FieldBinaryFileReadonly.include(
    {
        set_value: function(value)
        {
            var self = this;
            (new instance.web.Model('ir.attachment')).call(
                'get_binary_extension',
                [
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
                    var $element = self.$element.find('.oe-binary-preview');
                    if(openerp.attachment_preview.can_preview(extension))
                    {
                        $element.click(function()
                        {
                            openerp.attachment_preview.show_preview(
                                null,
                                _.str.sprintf(
                                    '/web/binary/saveas?session_id=%s&model=%s&field=%s&id=%d',
                                    instance.connection.session_id,
                                    self.view.dataset.model,
                                    self.name,
                                    self.view.datarecord.id),
                                extension,
                                self.view.datarecord[self.node.attrs.filename]);
                        });
                    }
                    else
                    {
                        $element.remove();
                    }
                });
            });
            return this._super.apply(this, arguments);
        },
    });
}    
