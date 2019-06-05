//-*- coding: utf-8 -*-
//Copyright 2018 Therp BV <https://therp.nl>
//License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

openerp.attachment_lock = function(instance)
{
    instance.web.Sidebar.include({
        init: function()
        {
            this._super.apply(this, arguments);
            this._extra_sidebar_attachment_fields.push('locked');
            this._extra_sidebar_attachment_fields.push('can_lock');
        },
        on_attachments_loaded: function()
        {
            var self = this;
            return jQuery.when(this._super.apply(this, arguments))
            .then(function()
            {
                self.$('.oe_sidebar_attachment_lock').click(
                    self.on_attachment_lock
                );
                self.$('.oe_sidebar_attachment_locked').click(
                    self.on_attachment_locked
                );
                self.$('.oe_sidebar_attachment_unlock').click(
                    self.on_attachment_unlock
                );
            });
        },
        on_attachment_lock: function(e)
        {
            var self = this;
            e.stopPropagation();
            return new instance.web.Model('ir.attachment')
            .call('lock', [[jQuery(e.currentTarget).data('id')]])
            .then(function()
            {
                return self.do_attachement_update(self.dataset, self.model_id);
            });
        },
        on_attachment_locked: function(e)
        {
            var self = this;
            e.stopPropagation();
            return new instance.web.Model('ir.attachment.lock')
            .query(['create_uid', 'valid_until'])
            .filter([['attachment_id', '=', jQuery(e.currentTarget).data('id')]])
            .first()
            .then(function(lock)
            {
                new instance.web.Dialog(
                    this, {
                        title: instance.web._t('Locked'),
                    },
                    $('<div/>').text(
                        _.str.sprintf(
                            instance.web._t('By %s until %s'),
                            lock.create_uid[1],
                            instance.web.format_value(lock.valid_until, {type: 'datetime'})
                        )
                    )
                ).open();
            });
        },
        on_attachment_unlock: function(e)
        {
            var self = this;
            e.stopPropagation();
            return new instance.web.Model('ir.attachment')
            .call('unlock', [[jQuery(e.currentTarget).data('id')]])
            .then(function()
            {
                return self.do_attachement_update(self.dataset, self.model_id);
            });
        },
    });
};
