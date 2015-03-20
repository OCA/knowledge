# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2015 Therp BV (<http://therp.nl>).
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
from openerp import http
from openerp.addons.web.controllers.main import Binary


class Binary(Binary):
    @http.route('/web/binary/upload_attachment', type='http', auth="user")
    def upload_attachment(self, callback, model, id, ufile, directory_id=None):
        if directory_id:
            # we can't use default_parent_id because of
            # the ir_attachment.create overwrite in document
            http.request.context['parent_id'] = int(directory_id)
            # fallback if the above is ever fixed
            http.request.context['default_parent_id'] = int(directory_id)
        return super(Binary, self).upload_attachment(
            callback, model, id, ufile)
