import {onWillStart, useState} from "@odoo/owl";
import {ControlPanel} from "@web/search/control_panel/control_panel";
import {browser} from "@web/core/browser/browser";
import {patch} from "@web/core/utils/patch";
import {useService} from "@web/core/utils/hooks";

patch(ControlPanel.prototype, {
    setup() {
        super.setup(...arguments);
        this.menuService = useService("menu");
        this.help = useState({content: false, canEdit: false});
        onWillStart(async () => {
            if (this.env.isSmall || (!this.helpActionId && !this.helpModel)) {
                return;
            }
            const help = await this.orm.call("help.section", "get_help", [
                this.helpActionId,
                this.helpModel,
            ]);
            this.help.content = help.has_help;
            this.help.canEdit = help.can_edit;
        });
    },

    get helpActionId() {
        return this.env.config.actionId || false;
    },

    get helpModel() {
        return this.env.searchModel?.resModel || false;
    },

    onClickHelp() {
        const params = new URLSearchParams({
            action_id: this.helpActionId || "",
            model: this.helpModel || "",
            menu_id: this.menuService.getCurrentApp()?.id || "",
        });
        // Same window name: the help window is reused
        const win = browser.open(
            `/screen_help?${params}`,
            "screen_help",
            "popup,width=900,height=750"
        );
        win?.focus();
    },
});
