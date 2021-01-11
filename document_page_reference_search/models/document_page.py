# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import re
from ast import literal_eval
from odoo import api, models, _
from odoo.exceptions import ValidationError


class DocumentPage(models.Model):
    _inherit = 'document.page'

    @api.constrains('reference')
    def _check_reference(self):
        super(DocumentPage, self)._check_reference()
        separator = self.env['ir.config_parameter'].get_param(
            'document.reference.separator'
        )
        for record in self:
            if separator and re.match(
                '^.*%s.*$' % separator, record.reference
            ):
                raise ValidationError(_(
                    'Reference cannot include the separator'))

    def _get_document(self, code):
        separator = self.env['ir.config_parameter'].get_param(
            'document.reference.separator'
        )
        if separator and re.match('^.*%s.*$' % separator, code):
            data = code.split(separator)
            rule = self.env['document.page.reference.rule'].search([
                ('name', '=', data[0])
            ])
            if not rule:
                return False
            element = self.env[rule.model_id.model].search([
                (rule.field_id.name, '=', data[1])
            ] + literal_eval(rule.extra_domain or '[]'), limit=1)
            if element:
                return element
            return False
        return super()._get_document(code)
