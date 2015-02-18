#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..backend import AbstractConnection
import sys
import os
from tempfile import TemporaryFile

class AbtractTask()

    def __init__(self, cr, uid):



class FileStoreConnection(AbstractTask):
    _key = "filestore"
    _name = "Filestore"
    _synchronize_type = None

    def __init__(self, host, user, pwd, port=None, allow_dir_creation=False):
        super(FilestoreConnection, self).__init__(host, user, pwd, port, allow_dir_creation)

    def connect(self):
        return NotImplemented

    def close(self):
        return NotImplemented

    def get(self, filename, path=None):
        if path:
            filepath = "{}/{}".format(path, filename)
        else:
            filepath = filename
        return open(filepath, 'r+b')

    def put(self, fileobject, filename, path=None):
        if path:
            filepath = "{}/{}".format(path, filename)
        else:
            filepath = filename
        output = open(filepath, 'w+b')
        return True

    def search(self, filename, path=None):
        if path:
            filepath = "{}/{}".format(path, filename)
        else:
            filepath = filename
        connection_list_result = os.listdir(filepath)
        return [x for x in connection_list_result if filename in x]

    def move(self, filename, oldpath, newpath):
        os.rename(
                os.path.join(oldpath, filename),
                os.path.join(newpath, filename)
                )

    def rename(self, oldfilename, newfilename, path=None):
        return NotImplemented

class ImportFileStore(FileStoreConnection):
    _synchronize_type = "import"


    def run():

