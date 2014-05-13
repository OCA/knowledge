# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2014 Savoir-faire Linux
#    (<http://www.savoirfairelinux.com>).
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

from openerp.osv import orm, fields


class metadata_list(orm.Model):
    _description = 'List of Metadata'
    _name = 'metadata.list'

    _columns = {
        'field_id': fields.many2one('ir.model.fields', 'Fields'),
        'metadata_id': fields.many2one('metadata', 'Metadata'),
    }


class metadata(orm.Model):
    _name = "metadata"
    _description = "Metadata"
    _columns = {
        'name': fields.char("Name", size=64, required=True, select=1),
        'model_id': fields.many2one('ir.model', 'Model',
                                    required=True, select=1),
        'field_ids': fields.many2many('ir.model.fields', 'metadata_field_rel',
                                      'meta_id', 'field_id', 'Fields'),
        'metadata_list_ids': fields.one2many('metadata.list', 'metadata_id',
                                             'List of fields'),
        'model_ids': fields.many2many('ir.model', string='Model List'),
    }

    def onchange_model(self, cr, uid, ids, model_id, context=None):
        if context is None:
            context = {}
        if not model_id:
            return {'value': {'model_ids': [(6, 0, [])]}}
        model_ids = [model_id]
        model_obj = self.pool.get('ir.model')
        active_model_obj = self.pool.get(model_obj.browse(
            cr, uid, model_id, context=context).model)
        if active_model_obj._inherits:
            for key, val in active_model_obj._inherits.items():
                found_model_ids = model_obj.search(cr,
                                                   uid, [('model', '=', key)],
                                                   context=context)
                model_ids += found_model_ids
        return {'value': {'model_ids': [(6, 0, model_ids)]}}

# vim:expandtab:smartindent:toabstop=4:softtabstop=4:shiftwidth=4:
