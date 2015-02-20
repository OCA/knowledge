#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
import os
from tempfile import TemporaryFile
from ftplib import FTP

class FTPConnection(object):

    def __init__(self, host, user, pwd, port=None, allow_dir_creation=False):
        super(FTPConnection, self).__init__(host, user, pwd, port, allow_dir_creation)
        if not port:
            self.port = 21
        self.protocol = "FTP"

    def connect(self):
        self.connection = FTP(self.location, self.port)
        self.connection.login(self.user, self.pwd)

    def close(self):
        self.connection.close()

    def get(self, filename, path=None):
        if path:
            filepath = "{}/{}".format(path, filename)
        else:
            filepath = filename
        outfile = TemporaryFile('w+b')
        self.connection.retrbinary('RETR ' + filepath, outfile.write)
        return outfile

    def put(self, fileobject, filename, path=None):
        if path:
            filepath = "{}/{}".format(path, filename)
        else:
            filepath = filename
        self.connection.storbinary('STOR ' + filepath, fileobject)
        return True

    def search(self, filename, path=None):
        if path:
            filepath = "{}/{}".format(path, filename)
        else:
            filepath = filename
        connection_list_result = self.connection.nlst()
        return [x for x in connection_list_result if filename in x]


    def move(self, filename, oldpath, newpath):
        self.connection.rename(
                os.path.join(oldpath, filename),
                os.path.join(newpath, filename)
                )

    def rename(self, oldfilename, newfilename, path=None):
        return NotImplemented
