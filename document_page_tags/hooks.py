# -*- coding: utf-8 -*-
##############################################################################
#
#    This module copyright (C) 2015 Therp BV <http://therp.nl>.
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
import re
from openerp import SUPERUSER_ID
from openerp.api import Environment


def post_init_hook(cr, pool):
    # in case we have an old tags column from the wiki module lying around,
    # populate our tags with its content
    for column in ['openupgrade_legacy_7_0_tags', 'tags']:
        cr.execute('SELECT column_name FROM information_schema.columns '
                   'WHERE table_name=%s and column_name=%s',
                   (pool['document.page']._table, column))
        if cr.fetchall():
            populate_tags(cr, column)


def populate_tags(cr, column):
    env = Environment(cr, SUPERUSER_ID, {})
    document_page_tag = env['document.page.tag']
    document_page = env['document.page']
    cr.execute(
        'SELECT %s, ARRAY_AGG(id) from %s WHERE %s IS NOT NULL GROUP BY %s' % (
            column, env['document.page']._table, column, column))
    for keywords, ids in cr.fetchall():
        pages = document_page.browse(ids)
        tag_ids = []
        for keyword in re.split(r'\W+', keywords):
            tag = document_page_tag.search([('name', '=ilike', keyword)])
            if tag:
                tag_ids.append(tag.id)
            else:
                tag_ids.append(document_page_tag.name_create(keyword)[0])
        pages.write({'tag_ids': [(6, 0, set(tag_ids))]})
