# -*- coding: utf-8 -*-
# © 2014 Serv. Tecnol. Avanzados (http://www.serviciosbaeza.com)
#                       Pedro M. Baeza <pedro.baeza@serviciosbaeza.com>
# © 2016 ACSONE SA/NV (<http://acsone.eu>)
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
        # Close client dialog
        return False
