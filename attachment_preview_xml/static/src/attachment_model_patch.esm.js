/** @odoo-module **/
/* Copyright 2026 Jarsa
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl). */

import {Attachment} from "@mail/core/common/attachment_model";
import {patch} from "@web/core/utils/patch";

patch(Attachment.prototype, {
    /**
     * XML attachments are stored with the ``text/plain`` mimetype for any user
     * without write access on views (see ``ir.attachment._check_contents``),
     * so the extension is the only reliable hint most of the time.
     */
    get isXml() {
        return (
            Boolean(this.id) &&
            !this.uploading &&
            ((this.extension || "").toLowerCase() === "xml" ||
                ["text/xml", "application/xml"].includes(this.mimetype))
        );
    },
    /**
     * XML files are rendered by our own viewer, not by the plain-text iframe.
     *
     * @override
     */
    get isText() {
        return super.isText && !this.isXml;
    },
    /**
     * @override
     */
    get isViewable() {
        return this.isXml || super.isViewable;
    },
});
