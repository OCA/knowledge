from odoo import http
from odoo.http import request


class ScreenHelp(http.Controller):
    def _dark(self):
        # "light" in community: dark only with a color scheme module,
        # e.g. web_dark_mode (OCA) or web_enterprise: preference of the user
        return request.env["ir.http"].color_scheme() == "dark"

    def _response(self, html):
        return request.make_response(
            html, headers=[("Content-Type", "text/html; charset=utf-8")]
        )

    @http.route("/screen_help", type="http", auth="user")
    def help(self, action_id=None, model=None, menu_id=None):
        """Help of a screen (action and / or model), shown in a window
        detached from the Odoo tab"""
        env = request.env
        action = env["ir.actions.act_window"].browse(int(action_id or 0)).exists()
        model = model or action.res_model
        if action:
            title, prefix = action.name, f"help_{action.id}"
        else:
            title, prefix = env["ir.model"]._get(model).name or model, "help"
        body, toc = env["help.section"]._for(action, model)._html(prefix)
        html = env["ir.actions.report"]._render_template(
            "screen_help.screen_help_page",
            {
                "title": title,
                "body": body,
                "toc": toc,
                "menu_id": int(menu_id) if menu_id else False,
                "dark": self._dark(),
                # edit button: sends the screen to the Odoo tab (help_service.esm.js)
                "can_edit": env.user.has_group("screen_help.group_editor"),
                "action_id": action.id,
                "model": model,
            },
        )
        return self._response(html)

    @http.route("/screen_help/app/<int:menu_id>", type="http", auth="user")
    def app_help(self, menu_id):
        """Help of all the screens of an application (root menu)"""
        html, __ = request.env["ir.actions.report"]._render_qweb_html(
            "screen_help.action_report_help_menu",
            [menu_id],
            data={"dark": self._dark()},
        )
        return self._response(html)
