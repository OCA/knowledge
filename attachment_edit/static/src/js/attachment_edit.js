//-*- coding: utf-8 -*-
//############################################################################
//
//   OpenERP, Open Source Management Solution
//   This module copyright (C) 2015 Therp BV <http://therp.nl>.
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

openerp.attachment_edit = function(instance)
{
    instance.web.Sidebar.include(
    {
        on_attachments_loaded: function(attachments)
        {
            var result = this._super.apply(this, arguments);    
            this.$el.find('.oe-sidebar-attachment-edit')
                .click(this.on_attachment_edit);
            return result;
        },
        on_attachment_edit: function(e)
        {
            var $target = jQuery(e.currentTarget),
                attachment_id = parseInt($target.attr('data-id')),
                title = $target.attr('title');
            e.preventDefault();
            e.stopPropagation();
            this.do_action({
                type: 'ir_actions.act_window',
                name: title,
                views: [[false, 'form']],
                res_model: 'ir.attachment',
                res_id: attachment_id,
                flags: {
                    initial_mode: 'edit',
                },
            });
        },
    })
}
