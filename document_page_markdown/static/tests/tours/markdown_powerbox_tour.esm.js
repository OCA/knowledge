/** @odoo-module **/

import tour from "web_tour.tour";

/**
 * Type in the editable the way a user would, so the editor reacts to it.
 *
 * @param {String} text
 */
function typeInEditor(text) {
    for (const character of text) {
        document.execCommand("insertText", false, character);
    }
}

tour.register(
    "document_page_markdown_powerbox_tour",
    {
        test: true,
    },
    [
        {
            content: "Open the powerbox and look for the Markdown entry",
            trigger: ".odoo-editor-editable > p",
            run: function () {
                const paragraph = this.$anchor[0];
                paragraph.focus();
                const range = document.createRange();
                range.selectNodeContents(paragraph);
                range.collapse(false);
                const selection = document.getSelection();
                selection.removeAllRanges();
                selection.addRange(range);
                typeInEditor("/markdown");
            },
        },
        {
            content: "Pick the Markdown entry",
            trigger:
                ".oe-powerbox-commandWrapper:has(.oe-powerbox-commandName:contains('Markdown'))",
        },
        {
            content: "Write some Markdown",
            trigger: ".o_markdown_dialog textarea.o_markdown_source",
            run: "text ## Inserted heading",
        },
        {
            content: "Check the preview tab",
            trigger: ".o_markdown_tabs a[data-tab='preview']",
        },
        {
            content: "The preview shows the formatted text",
            trigger: ".o_markdown_preview h2:contains('Inserted heading')",
            isCheck: true,
        },
        {
            content: "Insert it in the page",
            trigger: "footer button.btn-primary",
        },
        {
            content: "The Markdown was inserted as content",
            trigger: ".odoo-editor-editable h2:contains('Inserted heading')",
            isCheck: true,
        },
        {
            content: "Save the page",
            trigger: ".o_form_button_save",
        },
        {
            content: "The record is saved",
            trigger: ".o_form_saved",
            isCheck: true,
        },
    ]
);
