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
import pytz
import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta
from openerp.osv.orm import Model
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT


class IrAttachment(Model):
    _inherit = 'ir.attachment'

    def _attachments_to_filesystem_init(self, cr, uid, context=None):
        """Set up config parameter and cron job"""
        module_name = __name__.split('.')[-3]
        ir_model_data = self.pool['ir.model.data']
        ir_cron = self.pool['ir.cron']
        location = self.pool['ir.config_parameter'].get_param(
            cr, uid, 'ir_attachment.location')
        if location:
            # we assume the user knows what she's doing. Might be file:, but
            # also whatever other scheme shouldn't matter. We want to bring
            # data from the database to there
            pass
        else:
            ir_model_data._update(
                cr, uid, 'ir.config_parameter', module_name,
                {
                    'key': 'ir_attachment.location',
                    'value': 'file',
                },
                xml_id='config_parameter_ir_attachment_location',
                context=context)

        # synchronous behavior
        if self.pool['ir.config_parameter'].get_param(
                cr, uid, 'attachments_to_filesystem.move_during_init'):
            self._attachments_to_filesystem_cron(cr, uid, context, limit=None)
            return

        # otherwise, configure our cronjob to run next night
        user = self.pool['res.users'].browse(cr, uid, uid, context=context)
        next_night = datetime.now() + relativedelta(
            hour=01, minute=42, second=0)
        next_night = pytz.timezone(user.tz).localize(next_night).astimezone(
            pytz.utc).replace(tzinfo=None)
        if next_night < datetime.now():
            next_night += relativedelta(days=1)
        ir_cron.write(
            cr, uid,
            [
                ir_model_data.get_object_reference(
                    cr, uid, module_name, 'cron_move_attachments')[1],
            ],
            {
                'nextcall':
                next_night.strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                'doall': True,
                'interval_type': 'days',
                'interval_number': 1,
            },
            context=context)

    def _attachments_to_filesystem_cron(self, cr, uid, context=None,
                                        limit=10000):
        """Do the actual moving"""
        limit = int(
            self.pool['ir.config_parameter'].get_param(
                cr, uid, 'attachments_to_filesystem.limit', '0')) or limit
        ir_attachment = self.pool['ir.attachment']
        attachment_ids = ir_attachment.search(
            cr, uid, [('db_datas', '!=', False)], limit=limit, context=context)
        logging.info('moving %d attachments to filestore', len(attachment_ids))
        # attachments can be big, so we read every attachment on its own
        for counter, attachment_id in enumerate(attachment_ids, start=1):
            attachment_data = ir_attachment.read(
                cr, uid, [attachment_id], ['datas', 'res_model'],
                context=context)[0]
            if attachment_data['res_model'] and not self.pool.get(
                    attachment_data['res_model']):
                logging.warning(
                    'not moving attachment %d because it links to unknown '
                    'model %s', attachment_id, attachment_data['res_model'])
                continue
            ir_attachment.write(
                cr, uid, [attachment_id],
                {
                    'datas': attachment_data['datas'],
                    'db_datas': False,
                },
                context=context)
            if not counter % (len(attachment_ids) / 100 or limit):
                logging.info('moving attachments: %d done', counter)
