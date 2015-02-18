# -*- coding: utf-8 -*-
###############################################################################
#
#   Module for OpenERP
#   Copyright (C) 2014 Akretion (http://www.akretion.com).
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

import sys
from openerp import models, fields

class Task(models.Model):
    _name = 'ir.location.task'
    _description = 'Description'
    
    name = fields.Char()
    method = fields.Selection([
        ('ftp_import', 'FTP import'),
        ('ftp_export', 'FTP export'),
        ('sftp_import', 'SFTP import'),
        ('sftp_export', 'SFTP export'),
        ('filestore_import', 'Filestore import'),
        ('filestore_export', 'Filestore export'),
        ])
    filename = fields.Char()
    filepath = fields.Char()
    location_id = fields.Many2one('ir.location', string='Location')

    def run(self):
        connection_class = ...

        method_class = getattr(sys.modules[__name__], self.method)
        conn = method_class(config)
        conn.run()
