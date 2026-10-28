import {HtmlField, htmlField} from "@web/views/fields/html/html_field";
import {registry} from "@web/core/registry";
import {useExternalListener} from "@odoo/owl";
import {useService} from "@web/core/utils/hooks";

class DocumentPageReferenceField extends HtmlField {
    setup() {
        super.setup();
        this.orm = useService("orm");
        this.action = useService("action");
        // Delegate: one listener that resolves the link at click time, so it
        // survives the html field re-rendering and is auto-removed on unmount.
        useExternalListener(document, "click", (event) => {
            const link = event.target.closest?.(".oe_direct_line");
            if (link) {
                this._onClickDirectLink(event, link);
            }
        });
    }
    _onClickDirectLink(event, link) {
        const {oeModel: model, oeId} = link.dataset;
        const id = parseInt(oeId, 10);
        if (!model || !id) {
            return;
        }
        event.preventDefault();
        this.orm.call(model, "get_formview_action", [[id]], {}).then((action) => {
            this.action.doAction(action);
        });
    }
}
registry.category("fields").add("document_page_reference", {
    ...htmlField,
    component: DocumentPageReferenceField,
});
