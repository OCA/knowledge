/** @odoo-module **/

import {HtmlField, htmlField} from "@web/views/fields/html/html_field";
import {registry} from "@web/core/registry";
import {onMounted, useRef} from "@odoo/owl";
import {useService} from "@web/core/utils/hooks";

class DocumentPageReferenceField extends HtmlField {
    setup() {
        super.setup();
        this.orm = useService("orm");
        this.action = useService("action");
        onMounted(() => {
            const links = document.querySelectorAll(".oe_direct_line");
            links.forEach((link) => {
                link.addEventListener("click", (event) =>
                    this._onClickDirectLink(event)
                );
            });
        });
    }
    _onClickDirectLink(event) {
        const {oeModel: model, oeId} = event.target.dataset;
        const id = parseInt(oeId, 10);
        this.orm.call(model, "get_formview_action", [[id]], {}).then((action) => {
            this.action.doAction(action);
        });
    }
}

registry.category("fields").add("document_page_reference", {
    ...htmlField,
    component: DocumentPageReferenceField,
});
