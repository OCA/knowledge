/** @odoo-module **/

import {Component, markup, useRef, useState, xml} from "@odoo/owl";
import {Dialog} from "@web/core/dialog/dialog";
import {_lt} from "@web/core/l10n/translation";
import {useService} from "@web/core/utils/hooks";
import {useWowlService} from "@web/legacy/utils";

const TOOLBAR_COMMANDS = [
    {name: "h1", icon: "fa-header", title: _lt("Heading"), prefix: "# "},
    {name: "h2", icon: "fa-header fa-sm", title: _lt("Subheading"), prefix: "## "},
    {name: "bold", icon: "fa-bold", title: _lt("Bold"), wrap: "**"},
    {name: "italic", icon: "fa-italic", title: _lt("Italic"), wrap: "*"},
    {name: "strike", icon: "fa-strikethrough", title: _lt("Strikethrough"), wrap: "~~"},
    {name: "code", icon: "fa-code", title: _lt("Code"), wrap: "`"},
    {name: "quote", icon: "fa-quote-right", title: _lt("Quote"), prefix: "> "},
    {name: "ul", icon: "fa-list-ul", title: _lt("Bulleted list"), prefix: "- "},
    {name: "ol", icon: "fa-list-ol", title: _lt("Numbered list"), prefix: "1. "},
    {
        name: "check",
        icon: "fa-check-square-o",
        title: _lt("Checklist"),
        prefix: "- [ ] ",
    },
    {name: "link", icon: "fa-link", title: _lt("Link"), template: "[$1](https://)"},
    {
        name: "table",
        icon: "fa-table",
        title: _lt("Table"),
        block: "| A | B |\n| --- | --- |\n|  |  |",
    },
    {name: "hr", icon: "fa-minus", title: _lt("Separator"), block: "---"},
];

/**
 * Write Markdown, preview it, and insert it as rich content.
 */
export class MarkdownDialog extends Component {
    setup() {
        this.orm = useService("orm");
        this.textareaRef = useRef("textarea");
        this.toolbar = TOOLBAR_COMMANDS;
        this.state = useState({source: "", preview: "", previewing: false});
    }

    /**
     * Apply a toolbar command on the current selection.
     *
     * @param {Object} command One of the entries of `TOOLBAR_COMMANDS`.
     */
    applyCommand(command) {
        const textarea = this.textareaRef.el;
        const value = textarea.value;
        let start = textarea.selectionStart;
        let end = textarea.selectionEnd;
        if (command.prefix) {
            // Line commands apply to the whole line(s) the cursor is on.
            start = value.lastIndexOf("\n", start - 1) + 1;
            const nextBreak = value.indexOf("\n", end);
            end = nextBreak === -1 ? value.length : nextBreak;
        }
        const selection = value.slice(start, end);
        let replacement = selection;
        if (command.wrap) {
            replacement = `${command.wrap}${selection}${command.wrap}`;
        } else if (command.prefix) {
            replacement = selection
                .split("\n")
                .map((line) => `${command.prefix}${line}`)
                .join("\n");
        } else if (command.template) {
            replacement = command.template.replace("$1", selection || _lt("label"));
        } else if (command.block) {
            const lineBreak = start === 0 || value[start - 1] === "\n" ? "" : "\n";
            replacement = `${lineBreak}${command.block}\n`;
        }
        textarea.value = value.slice(0, start) + replacement + value.slice(end);
        textarea.focus();
        const cursor = start + replacement.length;
        textarea.setSelectionRange(cursor, cursor);
        this.state.source = textarea.value;
    }

    onInput(ev) {
        this.state.source = ev.target.value;
    }

    /**
     * Switch between the "Write" and "Preview" tabs.
     *
     * @param {Boolean} previewing
     */
    async showTab(previewing) {
        this.state.previewing = previewing;
        if (previewing) {
            this.state.preview = markup(await this.renderMarkdown());
        }
    }

    renderMarkdown() {
        return this.orm.call("document.page", "render_markdown", [this.state.source]);
    }

    async onInsert() {
        if (this.state.source) {
            this.props.insert(await this.renderMarkdown());
        }
        this.props.close();
    }
}

MarkdownDialog.template = "document_page_markdown.MarkdownDialog";
MarkdownDialog.components = {Dialog};
MarkdownDialog.props = {
    insert: Function,
    // Injected by the dialog service.
    close: Function,
};

/**
 * Mountable wrapper, so the legacy wysiwyg widget can open the dialog.
 */
export class MarkdownDialogWrapper extends Component {
    setup() {
        useWowlService("dialog").add(MarkdownDialog, this.props);
    }
}

MarkdownDialogWrapper.template = xml``;
MarkdownDialogWrapper.props = {insert: Function};
