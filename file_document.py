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


class file_document(orm.Model):
    _inherit = "file.document"

    def _prepare_data_for_file_document(self, cr, uid, msg, context=None):
        """Method to prepare the data for creating a file document.
        :param msg: a dictionnary with the email data
        :type: dict

        :return: a list of dictionnary that containt the file document data
        :rtype: list
        """
        return []

    def message_new(self, cr, uid, msg, custom_values, context=None):
        created_ids = []
        res = self._prepare_data_for_file_document(cr, uid, msg, context=context)
        if res:
            for vals in res:
                if context.get('default_file_document_vals'):
                    vals.update(context['default_file_document_vals'])
                created_ids.append(self.create(cr, uid, vals, context=context))
                print "create message", vals['date']
            return created_ids
        return None
