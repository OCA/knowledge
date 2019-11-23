//-*- coding: utf-8 -*-
// (c) 2015-2018 Therp BV <http://therp.nl>
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
odoo.define('attachment_edit', function(require) {
    var Sidebar = require('web.Sidebar');

    Sidebar.include({
        on_attachments_loaded: function() {
            this._super.apply(this, arguments);
            this.$('.o_sidebar_edit_attachment')
                .click(this.proxy('on_attachment_edit'));
        },
        on_attachment_edit: function(e) {
            var $target = jQuery(e.currentTarget),
                attachment_id = parseInt($target.attr('data-id'), 10);
            e.preventDefault();
            e.stopPropagation();
            return this.do_action({
                type: 'ir_actions.act_window',
                views: [[false, 'form']],
                res_model: 'ir.attachment',
                res_id: attachment_id,
                flags: {
                    initial_mode: 'edit',
                },
            });
        },
    });
});
