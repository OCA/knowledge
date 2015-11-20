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
import logging
from openerp import models, api
_logger = logging.getLogger(__name__)


class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    @api.multi
    def document_reindex(self):
        for this in self:
            if not this.datas:
                continue
            try:
                mimetype, indexed_content = this._index(
                    this.datas.decode('base64'),
                    this.datas_fname, this.file_type)
                this.write({
                    'file_type': mimetype,
                    'index_content': indexed_content,
                })
            except:
                self.env.clear()
                self.env.clear_recompute_old()
                _logger.exception('ignoring attachment id %d', this.id)
                continue

    @api.model
    def document_reindex_domain(self, domain, limit=100, max_records=0):
        offset = 0
        limit = int(
            self.env['ir.config_parameter'].get_param(
                'document_reindex.limit', '0')) or limit
        logging.info(
            'reindexing %d attachments', self.search(domain, count=True))
        while True:
            attachments = self.search(domain, limit=limit, offset=offset)
            if not attachments:
                return
            attachments.document_reindex()
            logging.info('%d done', offset + len(attachments))
            offset += len(attachments)
            if max_records and offset > max_records:
                break

    @api.model
    def document_reindex_all(self):
        return self.document_reindex_domain([('type', '=', 'binary')])

    @api.model
    def document_reindex_unindexed(self):
        return self.document_reindex_domain([
            ('type', '=', 'binary'),
            '|',
            ('index_content', '=', False),
            ('index_content', '=', ''),
        ])
