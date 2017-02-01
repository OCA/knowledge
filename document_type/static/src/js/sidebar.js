odoo.define('document_type.sidebar', function(require) {
    "use strict";

    var core = require('web.core');
    var form_common = require('web.form_common');
    var Sidebar = require('web.Sidebar');
    var Dialog = require('web.Dialog');
    var Model = require('web.Model');

    var _t = core._t;

    Sidebar.include({

        do_attachement_update: function(dataset, model_id, args) {
            var self = this;
            // if args is defined, a new attachment has been added
            if (args && !args[0].error) {
                var pop = new form_common.FormViewDialog(self, {
                    res_model: 'ir.attachment',
                    res_id: args[0].id,
                    title: _t('Set attachment details'),
                    view_id: self.attachment_upload_view_id
                }).open();
            }
            this._super.apply(this, arguments);
        },

        start: function() {
            var res = this._super.apply(this, arguments);
            var self = this;
            new Model('ir.model.data')
                .call('xmlid_to_res_id', ['document_type.ir_attachment_view_form_upload'])
                .then(function(view_id) {
                    self.attachment_upload_view_id = view_id;
                });
        }

    });

});
