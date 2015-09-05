# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2015 Therp BV (<http://therp.nl>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp import models, SUPERUSER_ID


class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    def _register_hook(self, cr):
        cr.execute(
            "select c.id from ir_model_constraint c, ir_model m "
            "where c.model=m.id and m.model='ir.attachment' and "
            "c.name='ir_attachment_filename_unique'")
        # this function does all the magic, but only if we select all
        # references to the constraint above, meaning all inheriting
        # module that also declare ir.attachment
        self.pool['ir.model.constraint']._module_data_uninstall(
            cr, SUPERUSER_ID, [i for i, in cr.fetchall()])
        return super(IrAttachment, self)._register_hook(cr)
