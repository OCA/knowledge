/** @odoo-module **/
/* Copyright 2026 Jarsa
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl). */

import {FileViewer} from "@web/core/file_viewer/file_viewer";
import {patch} from "@web/core/utils/patch";

patch(FileViewer.prototype, {
    setup() {
        super.setup();
        this._prepareOfficePreview();
    },
    /**
     * @override
     */
    activateFile(index) {
        super.activateFile(index);
        this._prepareOfficePreview();
    },
    /**
     * The PDF.js iframe gives no feedback while the server converts an office
     * document (which can take a while for big files). Warm the server-side
     * conversion cache with a plain fetch, showing a spinner meanwhile; once
     * it resolves the iframe is mounted and loads instantly from the cache.
     */
    _prepareOfficePreview() {
        const file = this.state.file;
        if (!file.isOffice) {
            this.state.officeLoading = false;
            return;
        }
        this.state.officeLoading = true;
        const done = () => {
            if (this.state.file === file) {
                this.state.officeLoading = false;
            }
        };
        fetch(file.officePdfUrl).then(done, done);
    },
});
