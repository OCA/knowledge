# -*- coding: utf-8 -*-
###############################################################################
#
#   file_email for OpenERP
#   Copyright (C) 2013 Akretion (http://www.akretion.com).
#   @author Sébastien BEAU <sebastien.beau@akretion.com>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as
#   published by the Free Software Foundation, either version 3 of the
#   License, or (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

from openerp.osv import fields, orm


class fetchmail_server(orm.Model):
    _inherit = 'fetchmail.server'

    def get_file_type(self, cr, uid, context=None):
        return []

    def _get_file_type(self, cr, uid, context=None):
        return self.get_file_type(cr, uid, context=context)

    _columns = {
        'file_type': fields.selection(_get_file_type, 'File Type',
                help='The file type will show some special option'),
        'company_id': fields.many2one('res.company', 'Company', required=True),#Why this field do not exist by default?
        'file_document_condition_ids': fields.one2many('prepare.file.document', 'server_id', 'File Document ')
    }

    _defaults = {
        'company_id': lambda s, cr, uid, c: s.pool.get('res.company')._company_default_get(cr, uid, 'fetchmail.server', context=c),
    }


    def get_context_for_server(self, cr, uid, server_id, context=None):
        if context is None:
            ctx = {}
        else:
            ctx = context.copy()
        ctx['default_file_document_vals'] = {}
        ctx['default_file_document_condition_ids'] = {}
        server = self.browse(cr, uid, server_id, context=context)
        ctx['default_company_id'] = server.company_id.id
        ctx['default_fetchmail_server_id'] = server_id
        ctx['default_file_document_condition_ids'] = [cond.id for cond in server.file_document_condition_ids]
        return ctx

    def fetch_mail(self, cr, uid, ids, context=None):
        for id in ids:
            ctx = self.get_context_for_server(cr, uid, id, context=context)
            super(fetchmail_server, self).fetch_mail(cr, uid, ids, context=ctx)
        return True
