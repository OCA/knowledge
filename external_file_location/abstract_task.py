#!/usr/bin/env python
# -*- coding: utf-8 -*-

from base64 import b64encode


class AbstractTask(object):

    def create_file(self, filename, data):
        ir_attachment_id = self.env['ir.attachment'].create(
                {
                    'name': filename,
                    'datas': b64encode(data),
                    'datas_fname': filename
                }
                )
        return ir_attachment_id

    # def load_file(self, file_id):
    #     f = self.session.browse('impexp.file', file_id)
    #     if not f.attachment_id.datas:
    #         return None
    #     return b64decode(f.attachment_id.datas)
