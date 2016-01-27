"""KnowledgeConfigSettings class."""
# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Business Applications
#    Copyright (C) 2004-2012 OpenERP S.A. (<http://openerp.com>).
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

from openerp import models, fields


class KnowledgeConfigSettings(models.TransientModel):
    """This class in needed to activate document management."""

    _name = 'knowledge.config.settings'
    _inherit = 'res.config.settings'

    module_document = fields.Boolean(
        'Manage documents',
        help='Document indexation, full text search of attachements.\n'
        '- This installs the module document.'
    )

    module_document_page = fields.Boolean(
        'Manage document pages (Wiki)',
        help='Provide document page and category as a wiki.\n'
        '- This installs the module document_page.'
    )

    module_document_page_approval = fields.Boolean(
        'Manage documents approval',
        help='Add workflow on documents per category.\n'
        '- This installs the module document_page_approval.'
    )

    module_cmis_read = fields.Boolean(
        'Attach files from an external DMS into Odoo',
        help='Connect Odoo with a CMIS compatible server to attach files\n'
        'to an Odoo record.\n'
        '- This installs the module cmis_read.'
    )

    module_cmis_write = fields.Boolean(
        'Store attachments in an external DMS instead of the Odoo Filestore',
        help='Connect Odoo with a CMIS compatible server to store files.\n'
        '- This installs the module cmis_write.'
    )
