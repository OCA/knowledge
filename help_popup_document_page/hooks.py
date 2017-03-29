# -*- coding: utf-8 -*-
# © 2017 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import SUPERUSER_ID, api


def post_init_hook(cr, pool):
    env = api.Environment(
        cr, SUPERUSER_ID, pool['res.users'].context_get(cr, SUPERUSER_ID)
    )
    for action in env['ir.actions.act_window'].search([
            '|',
            ('enduser_help', '!=', False),
            ('advanced_help', '!=', False),
    ]):
        if action.enduser_help and not action.enduser_document_page_ids:
            env['document.page'].create({
                'name': action.name,
                'parent_id':
                env.ref('help_popup_document_page.page_category').id,
                'help_popup_window_action_ids': [(4, action.id)],
                'content': action.enduser_help
            })
        if action.advanced_help and not action.advanced_document_page_ids:
            env['document.page'].create({
                'name': action.name,
                'parent_id':
                env.ref('help_popup_document_page.page_category').id,
                'help_popup_window_advanced_action_ids': [(4, action.id)],
                'content': action.advanced_help
            })
