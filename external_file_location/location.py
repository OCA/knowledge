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

from openerp import models, fields

class Location(models.Model):
    _name = 'ir.location'
    _description = 'Description'
    
    name = fields.Char(string='Name')
    protocol = fields.Selection(selection='_get_protocol')
    address = fields.Char(string='Address')
    port = fields.Integer()
    login = fields.Char()
    password = fields.Char()


    def _get_protocol(self):
        return [('ftp', 'FTP'), ('sftp', 'SFTP'), ('filestore', 'Filestore')]
                
