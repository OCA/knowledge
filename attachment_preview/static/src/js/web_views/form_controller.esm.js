/** @odoo-module **/
import {FormController} from "@web/views/form/form_controller";
import {patch} from "@web/core/utils/patch";

patch(FormController.prototype, "attachment_preview.FormController", {
    /* Defined in addons/mail/static/src/views/form/form_controller.js.
     * This method controls Odoo's default attachment sidebar, which only shows
     * up based on screen size. ➔ Superseded by this module; we disable it. */
    hasAttachmentViewer() {
        return false;
    },
});
