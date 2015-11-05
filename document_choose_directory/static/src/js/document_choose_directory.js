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

openerp.document_choose_directory = function(instance)
{
    instance.web.Sidebar.include(
    {
        init: function()
        {
            this._super.apply(this, arguments);
            this.directory_candidates = [];
        },
        do_attachement_update: function(dataset, model_id, args)
        {
            var document_folder = new instance.web.Model(
                'document.directory', dataset.get_context()),
                self = this,
                _super = this._super;
            return document_folder.call(
                'get_candidates_for_resource', [dataset.model, model_id])
                .then(function(records)
                {
                    self.directory_candidates = records;
                    self.$el.on(
                        //suppress html's onclick event that would close the
                        //menu
                        'click', 'select[name="directory_id"]',
                        function(e) {e.stopPropagation()});
                })
                .then(function()
                {
                    _super.apply(self, [dataset, model_id, args]);
                });
        },
        on_attachments_loaded: function(attachments)
        {
            var self = this,
                attachments_per_directory = [];
            _.chain(attachments)
                .groupBy(
                    function(a) { return a.parent_id[0] })
                .sortBy(function(attachments) {
                    return attachments[0].parent_id[1];
                })
                .each(
                    function(group)
                    {
                        attachments_per_directory.push({
                            name: _.first(group).parent_id[1] ||
                                instance.web._t('No directory'),
                            classname: 'oe_attachment_directory',
                        });
                        self.sort_attachments(group).each(function(a)
                        {
                            attachments_per_directory.push(a);
                        });
                    });

            return this._super(attachments_per_directory);
        },
        get_directory_items: function(items)
        {
            return _(items).filter(
                function(i)
                {
                    return i.classname == 'oe_attachment_directory';
                });
        },
        sort_attachments: function(attachments)
        {
            return _.chain(attachments).sortBy('name');
        },
    });
}
