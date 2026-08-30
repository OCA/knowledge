# Copyright 2015-2018 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class DocumentPageTag(models.Model):
    _name = "document.page.tag"
    _description = "A keyword for document pages"
    _parent_store = True

    name = fields.Char(required=True, translate=True)
    color = fields.Integer(string="Color Index")
    active = fields.Boolean(default=True)
    parent_id = fields.Many2one(
        "document.page.tag", string="Parent Tag", index=True, ondelete="restrict"
    )
    child_ids = fields.One2many("document.page.tag", "parent_id", string="Child Tags")
    parent_path = fields.Char(index=True)

    _sql_constraints = [
        ("unique_name", "unique(name)", "Tags must be unique"),
    ]

    @api.constrains("parent_id")
    def _check_parent_id(self):
        if self._has_cycle():  # pragma: no cover
            raise ValidationError(_("You can not create recursive tags."))

    def _get_hierarchy_name(self):
        self.ensure_one()
        names = []
        tag = self
        while tag:
            names.append(tag.name or "")
            tag = tag.parent_id
        return " / ".join(reversed(names))

    @api.depends("parent_id")
    def _compute_display_name(self):
        for tag in self:
            tag.display_name = tag._get_hierarchy_name()

    @api.model
    def _search_display_name(self, operator, value):
        domain = super()._search_display_name(operator, value)
        if operator.endswith("like"):
            return [("id", "child_of", self._search(list(domain)))]
        return domain

    @api.model_create_multi
    def create(self, vals_list):
        """Be nice when trying to create duplicates"""
        records = self.env["document.page.tag"]
        for vals in vals_list:
            existing = self.search([("name", "=ilike", vals.get("name"))], limit=1)
            if existing:
                records |= existing
            else:
                records |= super().create([vals])
        return records
