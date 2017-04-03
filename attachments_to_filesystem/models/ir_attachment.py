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
from openerp import api, fields, models


class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    @api.model
    def _attachments_to_filesystem_init(self):
        """Set up config parameter and cron job"""
        module_name = __name__.split('.')[-3]
        ir_model_data = self.env['ir.model.data']
        location = self.env['ir.config_parameter'].get_param(
            'ir_attachment.location'
        )
        if location:
            # we assume the user knows what she's doing. Might be file:, but
            # also whatever other scheme shouldn't matter. We want to bring
            # data from the database to there
            pass
        else:
            ir_model_data._update(
                'ir.config_parameter', module_name,
                {
                    'key': 'ir_attachment.location',
                    'value': 'file',
                },
                xml_id='config_parameter_ir_attachment_location'
            )

        # synchronous behavior
        if self.env['ir.config_parameter'].get_param(
                'attachments_to_filesystem.move_during_init'
        ):
            self._attachments_to_filesystem_cron(limit=None)
            return

        # otherwise, configure our cronjob to run next night
        user = self.env.user
        next_night = datetime.now() + relativedelta(
            hour=01, minute=42, second=0)
        user_tz = user.tz or 'UTC'
        next_night = pytz.timezone(user_tz).localize(next_night).astimezone(
            pytz.utc).replace(tzinfo=None)
        if next_night < datetime.now():
            next_night += relativedelta(days=1)
        self.env.ref('%s.cron_move_attachments' % module_name).write({
            'nextcall': fields.Datetime.to_string(next_night),
            'doall': True,
            'interval_type': 'days',
            'interval_number': 1,
        })

    @api.model
    def _attachments_to_filesystem_cron(self, limit=10000):
        """Do the actual moving"""
        limit = int(
            self.env['ir.config_parameter'].get_param(
                'attachments_to_filesystem.limit', '0')) or limit
        ir_attachment = self.env['ir.attachment']
        attachment_ids = ir_attachment.search(
            [('db_datas', '!=', False)], limit=limit)
        logging.info('moving %d attachments to filestore', len(attachment_ids))
        # attachments can be big, so we read every attachment on its own
        for counter, attachment_id in enumerate(attachment_ids, start=1):
            attachment_data = ir_attachment.read(
                [attachment_id], ['datas', 'res_model']
            )[0]
            if attachment_data['res_model'] and not self.env.registry.get(
                    attachment_data['res_model']):
                logging.warning(
                    'not moving attachment %d because it links to unknown '
                    'model %s', attachment_id, attachment_data['res_model'])
                continue
            try:
                ir_attachment.write(
                    [attachment_id],
                    {
                        'datas': attachment_data['datas'],
                        'db_datas': False,
                    })
            except Exception:
                logging.exception('Error moving attachment #%d', attachment_id)
            if not counter % (len(attachment_ids) / 100 or limit):
                logging.info('moving attachments: %d done', counter)
