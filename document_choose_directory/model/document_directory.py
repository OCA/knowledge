# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2014 Therp BV (<http://therp.nl>).
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
from openerp.osv.orm import Model


class DocumentDirectory(Model):
    _inherit = 'document.directory'

    def _get_candidates_for_resource(self, cr, uid, res_model, res_id,
                                     context=None):
        '''return directories that can be chosen for a certain record of a
        certain model - called by js api, override as needed'''
        result = []
        for this in self.browse(
                cr, uid,
                self.search(
                    cr, uid,
                    [
                        ('type', '=', 'directory'),
                        ('ressource_type_id.model', '=', res_model),
                    ],
                    context=context),
                context=context):
            result.append(this)
        return result

    def get_candidates_for_resource(self, cr, uid, res_model, res_id,
                                    context=None):
        '''return directories that can be chosen for a certain record of a
        certain model - js api'''
        result = []
        for this in self._get_candidates_for_resource(
                cr, uid, res_model, res_id, context=context):
            result.append({
                'id': this.id,
                'name': this.name_get()[0][1],
            })
        return result

    def _register_hook(self, cr):
        from openerp.addons.web.http import httprequest
        from openerp.addons.web.controllers.main import Binary
        original = Binary.upload_attachment

        @httprequest
        def upload_attachment(self, req, callback, model, id, ufile,
                              directory_id=None):
            if directory_id:
                # we can't use default_parent_id because of
                # the ir_attachment.create overwrite in document
                req.context['parent_id'] = int(directory_id)
                # fallback if the aboev is ever fixed
                req.context['default_parent_id'] = int(directory_id)
            return original(self, req, callback, model, id, ufile)

        Binary.upload_attachment = upload_attachment
