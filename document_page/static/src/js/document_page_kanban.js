odoo.define("document_page.update_kanban", function(require) {
    "use strict";
    
    var KanbanRecord = require("web.KanbanRecord");

    KanbanRecord.include({
        // --------------------------------------------------------------------------
        // Private
        // --------------------------------------------------------------------------

        /**
         * @override
         * @private
         */
        _openRecord: function() {
            if (
                this.modelName === "document.page" &&
                this.$(".o_document_page_kanban_boxes a").length
            ) {
                this.$(".o_document_page_kanban_boxes a")
                    .first()
                    .click();
            } else {
                this._super.apply(this, arguments);
            }
        }
    });
});
