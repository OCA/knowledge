/** @odoo-module **/
/* Copyright 2026 Jarsa
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl). */

import {Attachment} from "@mail/core/common/attachment_model";
import {patch} from "@web/core/utils/patch";
import {session} from "@web/session";
import {url} from "@web/core/utils/urls";

export const OFFICE_EXTENSIONS = [
    "doc",
    "docm",
    "docx",
    "odg",
    "odp",
    "ods",
    "odt",
    "ppt",
    "pptm",
    "pptx",
    "xls",
    "xlsm",
    "xlsx",
];

patch(Attachment.prototype, {
    get isOffice() {
        return (
            Boolean(session.attachment_preview_office_available) &&
            Boolean(this.id) &&
            !this.uploading &&
            OFFICE_EXTENSIONS.includes((this.extension || "").toLowerCase())
        );
    },
    /**
     * Office files are previewed as PDF (server-side LibreOffice conversion),
     * so the native PDF.js viewer branch of FileViewer renders them.
     *
     * @override
     */
    get isPdf() {
        return super.isPdf || this.isOffice;
    },
    /**
     * Raw URL of the server-side PDF conversion of this office attachment.
     */
    get officePdfUrl() {
        return url("/attachment_preview_office/to_pdf", {
            model: "ir.attachment",
            field: "datas",
            id: this.id,
            filename: this.displayName || `file.${this.extension}`,
        });
    },
    /**
     * @override
     */
    get defaultSource() {
        if (!this.isOffice) {
            return super.defaultSource;
        }
        return `/web/static/lib/pdfjs/web/viewer.html?file=${encodeURIComponent(
            this.officePdfUrl
        )}#pagemode=none`;
    },
});
