#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..backend import AbstractTask
import sys
import os
from tempfile import TemporaryFile


class FileStore(AbstractTask):
    _key = "filestore"
    _name = "Filestore"
    _synchronize_type = None

    def __init__(self, config):
        # super(FilestoreConnection, self).__init__(host, user, pwd, port, allow_dir_creation)
        self.host = config.get('host', '')
        self.user = config.get('user', '')
        self.pwd = config.get('pwd', '')
        self.port = config.get('port', '')
        self.allow_dir_creation = config.get('allow_dir_creation', '')
        self.filename = config.get('filename', '')
        self.path = config.get('path', '')

    def connect(self):
        return NotImplemented

    def close(self):
        return NotImplemented

    def get(self):
        if self.path:
            filepath = "{}/{}".format(self.path, self.filename)
        else:
            filepath = self.filename
        return open(filepath, 'r+b')

    def put(self):
        if self.path:
            filepath = "{}/{}".format(self.path, self.filename)
        else:
            filepath = self.filename
        output = open(filepath, 'w+b')
        return True

    def search(self):
        if self.path:
            filepath = "{}/{}".format(self.path, self.filename)
        else:
            filepath = self.filename
        connection_list_result = os.listdir(filepath)
        return [x for x in connection_list_result if filename in x]


class ImportFileStore(FileStore):
    _synchronize_type = "import"


    def run():
        self.connect()
        file = self.get(self.filename)
        self.close()
        return file

class ExportFileStore(FileStore):
    _synchronize_type = "export"


    def run():
        self.connect()
        self.put(self.filename)
        self.close()

