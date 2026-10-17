// Translation helper for the texts shown to the user
import {_t} from "@web/core/l10n/translation";
// Registry of Odoo: services are declared in its "services" category
import {registry} from "@web/core/registry";

// Service listening to the detached help window: its edit button sends a
// message to this Odoo tab, which opens the help sections to edit
export const helpPopupService = {
    // Services used by this one: action, to open the list of sections
    dependencies: ["action"],
    // Called once when the web client starts
    start(env, {action}) {
        // Listen to the messages sent to this tab (by other windows)
        window.addEventListener("message", (ev) => {
            // Only the messages of the same Odoo server, sent by our help window
            if (
                ev.origin !== window.location.origin ||
                ev.data?.type !== "screen_help_edit"
            ) {
                return;
            }
            // Action and model of the screen whose help is shown
            const {actionId, model} = ev.data;
            // Open the list of the help sections of this screen
            action.doAction({
                // Window action built on the fly
                type: "ir.actions.act_window",
                // Title of the list
                name: _t("Help Sections"),
                // Model of the records to show
                res_model: "help.section",
                // List view first, then form view (default views of the model)
                views: [
                    [false, "list"],
                    [false, "form"],
                ],
                // Sections of the action or of the model of the screen
                domain: ["|", ["action_id", "=", actionId], ["model", "=", model]],
                // New sections are linked to the action, when there is one
                context: {default_action_id: actionId},
            });
        });
    },
};

// Declare the service: started with the web client
registry.category("services").add("screen_help", helpPopupService);
