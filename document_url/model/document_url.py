# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (c) 2014 Serv. Tecnol. Avanzados (http://www.serviciosbaeza.com)
#                       Pedro M. Baeza <pedro.baeza@serviciosbaeza.com>
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
try:
    # Python 3
    from urllib import parse as urlparse
except:
    from urlparse import urlparse


class AddUrlWizard(orm.TransientModel):
    _name = 'ir.attachment.add_url'

    _columns = {
        'name': fields.char('Name', required=True),
        'url': fields.char('URL', required=True),
    }

    def action_add_url(self, cr, uid, ids, context=None):
        """Adds the URL with the given name as an ir.attachment record."""
        if context is None:
            context = {}
        if not context.get('active_model'):
            return
        attachment_obj = self.pool['ir.attachment']
        for form in self.browse(cr, uid, ids, context=context):
            url = urlparse(form.url)
            if not url.scheme:
                url = urlparse('%s%s' % ('http://', form.url))
            for active_id in context.get('active_ids', []):
                attachment = {
                    'name': form.name,
                    'type': 'url',
                    'url': url.geturl(),
                    'user_id': uid,
                    'res_id': active_id,
                    'res_model': context['active_model'],
                }
                attachment_obj.create(cr, uid, attachment, context=context)
        return {'type': 'ir.actions.act_close_wizard_and_reload_view'}
