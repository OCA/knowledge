#!/usr/bin/env python
# -*- coding: utf-8 -*-


#class AbstractConnection(object):
#
#    def __init__(self, host, user, pwd, port=None, allow_dir_creation=False):
#        self.host = host
#        self.user = user
#        self.pwd = pwd
#        self.port = port
#        self.allow_dir_creation = allow_dir_creation
#        self.connection = None
#
#    def connect(self):
#        return NotImplemented
#
#    def close(self):
#        return NotImplemented
#
#    def get(self, filename, path=None):
#        return NotImplemented
#
#    def put(self, fileobject, filename, path=None):
#        return NotImplemented
#
#    def search(self, filename, path=None):
#        return NotImplemented
#
#    def move(self, filename, oldpath, newpath):
#        return NotImplemented
#
#    def rename(self, oldfilename, newfilename, path=None):
#        return NotImplemented

class AbstractTask():

    
