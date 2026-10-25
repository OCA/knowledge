from odoo import http
from odoo.http import request


class ScreenHelp(http.Controller):
    @http.route("/screen_help", type="http", auth="user")
    def help(self, action_id=None, model=None, menu_id=None):
        env = request.env
        action = env["ir.actions.act_window"].browse(int(action_id or 0)).exists()
        model = model or action.res_model
        if action:
            title, prefix = action.name, f"help_{action.id}"
        else:
            title, prefix = env["ir.model"]._get(model).name or model, "help"
        body, toc = env["help.section"]._for(action, model)._html(prefix)
        return request.render(
            "screen_help.screen_help_page",
            {
                **env["ir.http"].webclient_rendering_context(),
                "title": title,
                "body": body,
                "toc": toc,
                "menu_id": int(menu_id) if menu_id else False,
                "can_edit": env.user.has_group("screen_help.group_editor"),
                "action_id": action.id,
                "model": model,
            },
        )

    @http.route("/screen_help/app/<int:menu_id>", type="http", auth="user")
    def app_help(self, menu_id):
        env = request.env
        menu = env["ir.ui.menu"].browse(menu_id).exists()
        if not menu:
            raise request.not_found()
        return request.render(
            "screen_help.app_help_page",
            {**env["ir.http"].webclient_rendering_context(), "menu": menu},
        )
