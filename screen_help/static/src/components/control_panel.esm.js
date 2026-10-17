// Browser wrapper of Odoo (window.open...), easier to mock in tests
import {browser} from "@web/core/browser/browser";
// Control panel: bar at the top of a view (breadcrumbs, pager, view switcher)
import {ControlPanel} from "@web/search/control_panel/control_panel";
// Function to extend an existing class without subclassing it
import {patch} from "@web/core/utils/patch";
// Hook giving access to Odoo services (menu, orm, action...)
import {useService} from "@web/core/utils/hooks";
// Reactive state, and hook running code before the first rendering
import {onWillStart, useState} from "@odoo/owl";

// Add the help buttons to every control panel
patch(ControlPanel.prototype, {
    // Called when a control panel is created
    setup() {
        // Keep the standard setup of the control panel
        super.setup(...arguments);
        // Menu service: knows the current application
        this.menuService = useService("menu");
        // Reactive state: the template is rendered again when it changes
        this.help = useState({content: false, canEdit: false});
        // Before the first rendering: ask the server whether there is help
        onWillStart(async () => {
            // No help buttons on mobile (small screen): no need to ask the server
            if (this.env.isSmall) {
                return;
            }
            // Screen without action nor model (e.g. client action): no help
            if (!this.helpActionId && !this.helpModel) {
                return;
            }
            // Call the python method help.section.get_help(action_id, model)
            const help = await this.orm.call("help.section", "get_help", [
                this.helpActionId,
                this.helpModel,
            ]);
            // Whether there is some help: shows the help (book) button
            this.help.content = help.has_help;
            // Whether the user may write the help: shows the button without help
            this.help.canEdit = help.can_edit;
        });
    },

    // Id of the window action shown (missing e.g. for a record opened by url)
    get helpActionId() {
        // False rather than undefined: sent as is to the server
        return this.env.config.actionId || false;
    },

    // Model of the records shown, to also get the help of the model
    get helpModel() {
        // The search model knows the model of the view (missing in some dialogs)
        return this.env.searchModel?.resModel || false;
    },

    // Click on the help (book) button: help in a window detached from the Odoo tab
    onClickHelp() {
        // Query string of the help page: action, model, current application
        const params = new URLSearchParams({
            // Window action shown (empty when none)
            action_id: this.helpActionId || "",
            // Model of the records shown
            model: this.helpModel || "",
            // Current application root menu, to offer its whole help
            menu_id: this.menuService.getCurrentApp()?.id || "",
        });
        // Same window name: the help window is reused instead of piling up
        const win = browser.open(
            `/screen_help?${params}`,
            "screen_help",
            "popup,width=900,height=750"
        );
        // Bring the help window to the front when it already existed
        win?.focus();
    },
});
