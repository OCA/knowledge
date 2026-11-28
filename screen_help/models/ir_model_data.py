from odoo import api, models


class IrModelData(models.Model):
    _inherit = "ir.model.data"

    @api.model
    def _process_end(self, modules):
        # load the help files of the installed / updated modules before the
        # records of these modules not loaded again are removed
        for module in modules:
            self.env["help.section"]._load_markdown(module)
        return super()._process_end(modules)
