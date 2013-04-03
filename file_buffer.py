# -*- coding: utf-8 -*-
###############################################################################
#
#   file_email for OpenERP
#   Copyright (C) 2012-TODAY Akretion <http://www.akretion.com>.
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


class file_buffer(orm.Model):
    _inherit = "file.buffer"

    def _prepare_data_for_file_buffer(self, cr, uid, msg, context=None):
        """Method to prepare the data for creating a file buffer.
        :param msg: a dictionnary with the email data
        :type: dict

        :return: a list of dictionnary that containt the file buffer data
        :rtype: list
        """
        return []

    def message_new(self, cr, uid, msg, custom_values, context=None):
        create_ids = []
        res = self._get_vals_for_file_buffer(cr, uid, msg, context=context)
        if res:
            for vals in res:
                file_id = self.create(cr, uid, vals, context=context)
                self.create_file_buffer_attachment(cr, uid, file_id,
                                                   datas, file_name,
                                                   context=context,
                                                   extension=vals['extension'])
                create_ids = file_id
            return create_ids
        return None
