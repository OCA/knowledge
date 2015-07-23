# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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
from openerp import models, fields, api


class document_page_create_menu(models.TransientModel):
    """ Create Menu """
    _name = "document.page.create.menu"
    _description = "Wizard Create Menu"

    menu_name = fields.Char(
        'Menu Name',
        required=True
    )

    menu_parent_id = fields.Many2one(
        'ir.ui.menu',
        'Parent Menu',
        required=True
    )

    @api.model
    def default_get(self, fields_list):
        res = super(document_page_create_menu, self).default_get(fields_list)
        page_id = self.env.context.get('active_id')
        obj_page = self.env['document.page']
        page = obj_page.browse(page_id)
        res['menu_name'] = page.name
        return res

    @api.multi
    def document_page_menu_create(self):
        obj_page = self.env['document.page']
        obj_menu = self.env['ir.ui.menu']
        obj_action = self.env['ir.actions.act_window']
        obj_model_data = self.env['ir.model.data']
        page_id = self.env.context.get('active_id', False)
        page = obj_page.browse(page_id)

        data = self[0]
        view_id = obj_model_data.sudo().get_object_reference(
            'document_page', 'view_wiki_menu_form')[1]
        value = {
            'name': 'Document Page',
            'view_type': 'form',
            'view_mode': 'form,tree',
            'res_model': 'document.page',
            'view_id': view_id,
            'type': 'ir.actions.act_window',
            'target': 'inlineview',
        }
        value['domain'] = "[('parent_id','=',%d)]" % (page.id)
        value['res_id'] = page.id

        # only the super user is allowed to create menu due to security rules
        # on ir.values
        # see.: http://goo.gl/Y99S7V
        action_id = obj_action.sudo().create(value)

        menu_id = obj_menu.sudo().create({
            'name': data.menu_name,
            'parent_id': data.menu_parent_id.id,
            'icon': 'STOCK_DIALOG_QUESTION',
            'action': 'ir.actions.act_window,' + str(action_id.id),
        })
        page.write({'menu_id': menu_id.id})
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
