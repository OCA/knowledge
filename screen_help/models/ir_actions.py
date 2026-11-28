from odoo import fields, models


class IrActionsActWindow(models.Model):
    _inherit = "ir.actions.act_window"

    help_section_ids = fields.One2many("help.section", "action_id")

    def _help_html(self):
        """Help of the action (sections of the action and of its model),
        with its table of contents (see help.section._html)"""
        self.ensure_one()
        return self.env["help.section"]._for(self)._html(f"help_{self.id}")
