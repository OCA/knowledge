import {_t} from "@web/core/l10n/translation";
import {registry} from "@web/core/registry";

// Edit button of the detached help window: opens the sections in this tab
export const screenHelpService = {
    dependencies: ["action"],
    start(env, {action}) {
        window.addEventListener("message", (ev) => {
            if (
                ev.origin !== window.location.origin ||
                ev.data?.type !== "screen_help_edit"
            ) {
                return;
            }
            const {actionId, model} = ev.data;
            action.doAction({
                type: "ir.actions.act_window",
                name: _t("Help Sections"),
                res_model: "help.section",
                views: [
                    [false, "list"],
                    [false, "form"],
                ],
                domain: ["|", ["action_id", "=", actionId], ["model", "=", model]],
                context: {default_action_id: actionId},
            });
        });
    },
};

registry.category("services").add("screen_help", screenHelpService);
