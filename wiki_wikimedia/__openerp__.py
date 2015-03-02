# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2012 Therp BV (<http://therp.nl>).
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
{
    'name': 'Wiki - wikimedia syntax',
    'version': '1.0',
    'category': 'Knowledge Management',
    'complexity': "normal",
    'description': """
    Replace the standard parser by one that understands (more) wikimedia syntax
    """,
    'author': "Therp BV,Odoo Community Association (OCA)",
    'website': 'http://therp.nl',
    'depends': ['wiki'],
    'init_xml': [],
    'installable': True,
    'auto_install': False,
    'js': ['static/src/lib/instaview.js', 'static/src/js/wiki_wikimedia.js'],
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
