/* Copyright 2014 Serv. Tecnol. Avanzados (http://www.serviciosbaeza.com)
 *                      Pedro M. Baeza <pedro.baeza@serviciosbaeza.com>
 * Copyright 2016 ACSONE SA/NV (<http://acsone.eu>)
 * Copyright 2019 Tecnativa - Ernesto Tejeda
 * Copyright 2020 Tecnativa - Manuel Calero
 * Copyright 2021 Tecnativa - Víctor Martínez
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
 */
odoo.define("document_url", function (require) {
    "use strict";

    const AttachmentBox = require("mail/static/src/components/attachment_box/attachment_box.js");
    const Attachment = require("mail/static/src/components/attachment/attachment.js");
    const {patch} = require("web.utils");

    patch(AttachmentBox, "document_url", {
        _onAddUrl() {
            this.env.bus.trigger("do-action", {
                action: "document_url.action_ir_attachment_add_url",
                options: {
                    additional_context: {
                        active_id: this.thread.id,
                        active_ids: [this.thread.id],
                        active_model: this.thread.model,
                    },
                    on_close: this._onAddedUrl.bind(this),
                },
            });
        },
        _onAddedUrl() {
            this.trigger("reload");
        },
    });
    patch(Attachment, "document_url", {
        _onClickImage(ev) {
            if (!this.attachment.isViewable) {
                this._onClickDownload(ev);
            }
            this._super.apply(this, arguments);
        },
    });
});
