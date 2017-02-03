odoo.define('attachment_attach_non_editable.sidebar', function(require) {
    "use strict";

    var core = require('web.core');
    var Sidebar = require('web.Sidebar');


    Sidebar.include({

        init: function(parent, options) {
            this._super.apply(this, arguments);
            if (parent.is_action_enabled('attach')) {
                this.options.attachable = true;
            }
        }

    });

});
