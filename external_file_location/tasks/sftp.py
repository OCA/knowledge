#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import paramiko
import os
from tempfile import TemporaryFile


class SFTPConnection(AbstractConnection):

    def __init__(self, host, user, pwd, port=None, allow_dir_creation=False):
        super(SFTPConnection, self).__init__(host, user, pwd, port, allow_dir_creation)
        if not port:
            self.port = 22
        self.protocol = "STFP"
    
    def connect(self):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(self.host, self.port, self.user, self.pwd, compress=True)
        self.connection = self.ssh.open_sftp()

    def close(self):
        self.connection.close()

    def get(self, filename, path=None):
        if path:
            remotefile = "{}/{}".format(path, filename)
        else:
            remotefile = filename
        localfile = filename
        newfile = open(filename, 'w')
        self.connection.getfo(remotefile, newfile)
        return newfile

    def put(self, fileobject, filename, path=None):
        if path:
            remotefile = "{}/{}".format(path, filename)
        else:
            remotefile = filename
        if self.allow_dir_creation:
            self.connection.mkdirs(path)
        oldfile = open(fileobj, 'r')
        self.connection.putfo(oldfile, remotefile)

    def search(self, filename, path=None):
        if path:
            self.connection.chdir(path)
        file_list = self.connection.listdir()
        return [x for x in file_list if filename in x]

    def move(self, filename, oldpath, newpath):
        self.connection.rename(os.path.join(oldpath, filename), os.path.join(newpath, filename))

    def rename(self, oldfilename, newfilename, path=None):
        if not path:
            path = ''
        self.connection.rename(os.path.join(path, oldfilename), os.path.join(path, newfilename))
