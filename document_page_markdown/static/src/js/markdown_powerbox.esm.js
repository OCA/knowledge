/** @odoo-module **/

import {
    parseHTML,
    preserveCursor,
} from "@web_editor/js/editor/odoo-editor/src/utils/utils";
import {ComponentWrapper} from "web.OwlCompatibility";
import {MarkdownDialogWrapper} from "@document_page_markdown/js/markdown_dialog.esm";
import Wysiwyg from "web_editor.wysiwyg";
import core from "web.core";

const _t = core._t;

/**
 * Add a "Markdown" entry to the editor's "/" powerbox, on knowledge pages.
 */
Wysiwyg.include({
    /**
     * @override
     */
    _getPowerboxOptions: function () {
        const options = this._super(...arguments);
        if (this.options.recordInfo.res_model !== "document.page") {
            return options;
        }
        options.commands.push({
            category: _t("Structure"),
            name: _t("Markdown"),
            priority: 25,
            description: _t("Write Markdown and insert it as content."),
            fontawesome: "fa-file-code-o",
            isDisabled: () => !this.odooEditor.isSelectionInBlockRoot(),
            callback: () => this._openMarkdownDialog(),
        });
        return options;
    },

    /**
     * Ask for a Markdown source and insert its rendering at the cursor.
     *
     * @private
     * @returns {Promise} resolved once the dialog is mounted
     */
    _openMarkdownDialog: function () {
        // Clicking in the dialog loses the selection inside the editable, so
        // it has to be restored before inserting anything.
        const restoreSelection = preserveCursor(this.odooEditor.document);
        const wrapper = new ComponentWrapper(this, MarkdownDialogWrapper, {
            insert: (html) => {
                restoreSelection();
                this.odooEditor.execCommand("insert", parseHTML(html));
            },
        });
        return wrapper.mount(document.body);
    },
});
