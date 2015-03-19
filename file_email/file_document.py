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
import base64


class file_document(orm.Model):
    _inherit = "file.document"

    _columns = {
        'fetchmail_server_id': fields.many2one('fetchmail.server', 'Email Server'),
    }



    def message_process(self, cr, uid, model, message, custom_values=None,
                        save_original=False, strip_attachments=False,
                        thread_id=None, context=None):
        if context is None:
            context = {}
        context['no_post'] = True
        return super(file_document, self).message_process(self, cr, uid, model,
                message,
                custom_values=custom_values,
                save_original=save_original,
                strip_attachments=strip_attachments,
                thread_id=thread_id,
                context=context)

    def message_post(self, cr, uid, thread_id, body='', subject=None, type='notification',
                        subtype=None, parent_id=False, attachments=None, context=None,
                        content_subtype='html', **kwargs):
        if context.get('no_post'):
            return None
        return super(file_document, self).message_post(cr, uid, thread_id,
                    body=body,
                    subject=subject,
                    type='notification',
                    subtype=subtype,
                    parent_id=parent_id,
                    attachments=attachments,
                    context=context,
                    content_subtype=content_subtype,
                    **kwargs)

    def _get_file_document_data(self, cr, uid, condition, msg, att, context=None):
        values = {
            'file_type': condition.server_id.file_type,
            'name': msg['subject'],
            'direction': 'input',
            'date': msg['date'],
            'ext_id': msg['message_id'],
            'datas_fname': att[0],
            'datas': base64.b64encode(att[1])
        }
        return values

    def prepare_data_from_basic_condition(self, cr, uid, condition, msg, context=None):
        vals = {}
        if condition.from_email in msg['from'] and condition.mail_subject in msg['subject']:
            for att in msg['attachments']:
                if condition.file_extension in att[0]:
                    vals = self._get_file_document_data(cr, uid, condition, msg, att, context=context)
                    break
        return vals


    def _prepare_data_for_file_document(self, cr, uid, msg, context=None):
        """Method to prepare the data for creating a file document.
        :param msg: a dictionnary with the email data
        :type: dict

        :return: a list of dictionnary that containt the file document data
        :rtype: list
        """
        res = []
        server_id = context.get('default_fetchmail_server_id', False)
        doc_file_condition_obj = self.pool.get('file.document.condition')
        cond_ids = doc_file_condition_obj.search(cr, uid, [('server_id', '=', server_id)])
        if cond_ids:
            for cond in doc_file_condition_obj.browse(cr, uid, cond_ids):
                if cond.type == 'normal':
                    vals = self.prepare_data_from_basic_condition(cr, uid, cond, msg, context=context)
                else:
                    vals = getattr(self, cond.type)(cr, uid, cond, msg, context=context)
                if vals:
                    res.append(vals) 
        return res

    def message_new(self, cr, uid, msg, custom_values, context=None):
        created_ids = []
        res = self._prepare_data_for_file_document(cr, uid, msg, context=context)
        if res:
            for vals in res:
                default = context.get('default_file_document_vals')
                if default:
                    for key in default:
                        if not key in vals:
                            vals[key] = default[key]
                created_ids.append(self.create(cr, uid, vals, context=context))
                cr.commit()
            context['created_ids'] = created_ids
            return created_ids[0]
        return None


class file_document_condition(orm.Model):
    _name = "file.document.condition"
    _description = "File Document Conditions"

    def _get_file_document_condition_type(self, cr, uid, context=None):
        return self.get_file_document_condition_type(cr, uid, context=context)

    def get_file_document_condition_type(self, cr, uid, context=None):
        return [('normal', 'Normal')]

    _columns = {
        'from_email': fields.char('Email', size=64),
        'mail_subject': fields.char('Mail Subject', size=64),
        'type': fields.selection(_get_file_document_condition_type,
               'Type', help="Create your own type if the normal type \
                            do not correspond to your need", required=True),
        'file_extension' : fields.char('File Extension', size=64, 
                                       help="File extension or file name",
                                       required=True),
        'server_id': fields.many2one('fetchmail.server', 'Server Mail'),
    }


    _defaults = {
        'type': 'normal'
    }

