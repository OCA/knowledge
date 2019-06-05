//-*- coding: utf-8 -*-
//Copyright 2018 Therp BV <https://therp.nl>
//License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

openerp.attachment_action = function(instance)
{
    instance.web.Sidebar.include({
        _extra_sidebar_attachment_fields: [],
        on_attachments_loaded: function(attachments)
        {
            var self = this, _super = this._super;
            return new instance.web.Model('ir.attachment')
            .query(this._extra_sidebar_attachment_fields)
            .filter([['id', 'in', _.pluck(attachments, 'id')]])
            .all()
            .then(function(extra_data)
            {
                _.each(attachments, function(attachment)
                {
                    _.extend(attachment, _.find(
                        extra_data, function(x)
                        {
                            return x.id == attachment.id
                        }
                    ));
                });
                _super.apply(self, [attachments]);
                return attachments;
            });
        },
    });
};
