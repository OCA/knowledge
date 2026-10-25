from odoo import models


class IrUiMenu(models.Model):
    _inherit = "ir.ui.menu"

    def _help_actions(self):
        """Window actions with help under these menus, in the menu order"""
        actions = self.env["ir.actions.act_window"]
        for menu in self:
            if menu.action and menu.action._name == "ir.actions.act_window":
                actions |= menu.action
            actions |= menu.child_id._help_actions()
        return actions.filtered(lambda a: self.env["help.section"]._for(a))

    def _help_html(self):
        """Help of the actions under the menu: [(action, html)], and its table
        of contents: one entry per action, followed by its headings.
        The actions are ordered by the lowest sequence of their sections,
        then by the menu order.
        The help of a model is shown once, with its first action."""
        self.ensure_one()
        Section = self.env["help.section"]
        actions = sorted(
            self._help_actions(),
            key=lambda a: min(Section._for(a).mapped("sequence")),
        )
        helps, toc, models_done = [], [], set()
        for action in actions:
            sections = Section._for(action)
            if action.res_model in models_done:
                sections = sections.filtered("action_id")
            if not sections:
                continue
            models_done.add(action.res_model)
            html, action_toc = sections._html(f"help_{action.id}")
            helps.append((action, html))
            toc.append((1, f"help_{action.id}", action.name))
            toc += action_toc
        return helps, toc
