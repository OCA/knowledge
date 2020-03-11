/* Copyright 2014 Serv. Tecnol. Avanzados (http://www.serviciosbaeza.com)
 *                      Pedro M. Baeza <pedro.baeza@serviciosbaeza.com>
 * Copyright 2016 ACSONE SA/NV (<http://acsone.eu>)
 * Copyright 2019 Tecnativa - Ernesto Tejeda
 * Copyright 2020 Tecnativa - Manuel Calero
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
 */
odoo.define("document_url", function(require) {
    "use strict";

    var AttachmentBox = require("mail.AttachmentBox");

    AttachmentBox.include({
        events: _.extend(AttachmentBox.prototype.events, {
            "click span.o_add_url_button": "_onAddUrl",
        }),
        _onAddUrl: function() {
            // Opens wizard to add an URL attachment to the current record
            this.do_action("document_url.action_ir_attachment_add_url", {
                additional_context: {
                    active_id: this.currentResID,
                    active_ids: [this.currentResID],
                    active_model: this.currentResModel,
                },
                on_close: this._onAddedUrl.bind(this),
            });
        },
        _onAddedUrl: function() {
            this.trigger_up("reload_attachment_box");
        },
    });
});
