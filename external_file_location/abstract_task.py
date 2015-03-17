#!/usr/bin/env python
# -*- coding: utf-8 -*-

from base64 import b64encode


class AbstractTask(object):

    def create_file(self, filename, data):
        ir_attachment_id = self.env['ir.attachment.metadata'].create({
            'name': filename,
            'datas': b64encode(data),
            'datas_fname': filename,
            'task_id': self.task.id,
            'location_id': self.task.location_id.id,
            'external_hash': self.ext_hash
            })
        return ir_attachment_id
