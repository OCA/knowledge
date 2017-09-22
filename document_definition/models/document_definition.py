# -*- coding: utf-8 -*-
# © 2017 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import api, fields, models


class DocumentDefinition(models.Model):
    _name = 'document.definition'

    term = fields.Char(help='Term to define', required=True)
    definition = fields.Text(help='Definition of term', required=True)

    # stored compute field used for making the letter grouping
    # need to be stored in order to use grouping
    first_letter = fields.Char()

    def _get_first_letter(self, text):
        # if somehow the user starts with a blank space we trim it
        return text.lstrip()[:1].upper() or 'Blank Term'

    @api.model
    def create(self, vals):
        vals['first_letter'] = self._get_first_letter(vals['term'])
        res = super(DocumentDefinition, self).create(vals=vals)
        return res

    @api.multi
    def write(self, vals):
        for this in self:
            if vals.get('term'):
                vals['first_letter'] = this._get_first_letter(vals['term'])
            res = super(DocumentDefinition, this).write(vals=vals)
        return res

    # constraint of uniqueness on term, two terms can't have different
    # definitions

    _sql_constraints = [('term_uniq', 'UNIQUE(term)',
                         'Every term must be unique')]
