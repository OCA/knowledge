# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2013 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
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

from openerp.osv import fields, orm


class document_page_history(orm.Model):
    _inherit = 'document.page.history'
    _columns = {
        'company_id': fields.many2one('res.company', 'Company')
    }

    _defaults = {
        'company_id': lambda self, cr, uid, c: self.pool.get('res.company')
        ._company_default_get(cr, uid, 'document_page_history', context=c)
    }


class document_page(orm.Model):
    _inherit = 'document.page'
    _columns = {
        'company_id': fields.many2one('res.company', 'Company')
    }

    _defaults = {
        'company_id': lambda self, cr, uid, c: self.pool.get('res.company')
        ._company_default_get(cr, uid, 'document_page', context=c)
    }

