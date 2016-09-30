/* © 2014 Serv. Tecnol. Avanzados (http://www.serviciosbaeza.com)
 *                      Pedro M. Baeza <pedro.baeza@serviciosbaeza.com>
 * © 2016 ACSONE SA/NV (<http://acsone.eu>)
 * Copyright 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
 */
odoo.define('document_url', function(require) {
    "use strict";
    var Sidebar = require('web.Sidebar');

    Sidebar.include({
        init: function (parent, options) {
            var result = this._super(parent, options);
            this.items.url_doc = [
                {
                    action: {
                        id: "document_url.action_ir_attachment_add_url",
                    },
                },
            ];
            return result;
        },

        redraw: function () {
            var result = this._super();
            // Open URLs in a different browser tab
            this.$el.find("a[href]").attr('target', '_blank');
            return result;
        },
    });
});
