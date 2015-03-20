# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2014 Therp BV (<http://therp.nl>).
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
from openerp.osv.orm import Model


class IrAttachment(Model):
    _inherit = 'ir.attachment'

    def read(self, cr, uid, ids, fields_to_read=None, context=None,
             load='_classic_read'):
        '''inject the extra field we need in the web client. This saves us a
        couple of extra client side calls'''
        if set(fields_to_read).issuperset(
                ['name', 'url', 'type', 'create_uid', 'create_date',
                 'write_uid', 'write_date']):
            fields_to_read = fields_to_read + ['parent_id']
        result = super(IrAttachment, self).read(
            cr, uid, ids, fields_to_read=fields_to_read, context=context,
            load=load)
        return result
