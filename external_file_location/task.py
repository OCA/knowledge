# -*- coding: utf-8 -*-
###############################################################################
#
#   Module for OpenERP
#   Copyright (C) 2015 Akretion (http://www.akretion.com).
#   @author Valentin CHEMIERE <valentin.chemiere@akretion.com>
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

from openerp import models, fields, api
from helper import itersubclasses
from abstract_task import AbstractTask


class Task(models.Model):
    _name = 'ir.location.task'
    _description = 'Description'

    name = fields.Char()
    method = fields.Selection(selection='_get_method')
    filename = fields.Char()
    filepath = fields.Char()
    location_id = fields.Many2one('external.file.location', string='Location')
    attachment_id = fields.Many2one('ir.attachment', string='Attachment')

    def _get_method(self):
        res = []
        for cls in itersubclasses(AbstractTask):
            if cls._synchronize_type:
                cls_info = (cls._key + '_' + cls._synchronize_type,
                            cls._name + ' ' + cls._synchronize_type)
                res.append(cls_info)
        return res

    @api.multi
    def run(self):
        for cls in itersubclasses(AbstractTask):
            if cls._synchronize_type and \
              cls._key + '_' + cls._synchronize_type == self.method:
                method_class = cls
        config = {
                'host': self.location_id.address,
                'user': self.location_id.login,
                'pwd': self.location_id.password,
                'port': self.location_id.port,
                'allow_dir_creation': False,
                'file_name': self.filename,
                'path': self.filepath,
                'attachment_id': self.attachment_id,
                }
        conn = method_class(self.env, config)
        conn.run()
