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

class document_page_history_wkfl(orm.Model):
    _inherit = 'document.page.history'
    _columns = {
        'state': fields.selection([
            ('draft','Draft'),
            ('approved','Approved')], 'Status', readonly=True),
        }
    
    def page_approval_draft(self, cr, uid, ids):
        self.write(cr, uid, ids, { 'state' : 'draft' })
        return True
    
    def page_approval_approved(self, cr, uid, ids):
        self.write(cr, uid, ids, { 'state' : 'approved' })
        return True
        
        
class document_page_approval(orm.Model):
    _inherit = 'document.page'
    def _get_display_content(self, cr, uid, ids, name, args, context=None):
        res = {}
        for page in self.browse(cr, uid, ids, context=context):
            if page.type == "category":
               content = self._get_page_index(cr, uid, page, link=False)
            else:
               content = page.content
            res[page.id] =  content
        return res
            
    _columns = {
        'display_content': fields.function(_get_display_content, string='Displayed Content', type='text')
    }
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
