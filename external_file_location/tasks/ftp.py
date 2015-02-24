# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 initOS GmbH & Co. KG (<http://www.initos.com>).
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

from ..abstract_task import AbstractTask
from base64 import b64decode
import ftputil
import ftputil.session
import logging
_logger = logging.getLogger(__name__)


class FtpTask(AbstractTask):

    _key = 'ftp'
    _name = 'FTP'
    _synchronize_type = None

    def __init__(self, env, config):
        self.env = env
        self.host = config.get('host', '')
        self.user = config.get('user', '')
        self.pwd = config.get('pwd', '')
        self.port = config.get('port', '')
        self.allow_dir_creation = config.get('allow_dir_creation', '')
        self.file_name = config.get('file_name', '')
        self.path = config.get('path', '')
        self.move_path = config.get('move_path', '')
        self.delete_file = config.get('delete_file', False)


class FtpImportTask(FtpTask):
    """FTP Configuration options:
     - host, user, password, port
     - download_directory:  directory on the FTP server where files are
                            downloaded from
     - move_directory:  If present, files will be moved to this directory
                        on the FTP server after download.
     - delete_files:  If true, files will be deleted on the FTP server
                      after download.
    """

    _synchronize_type = 'import'

    def _handle_new_source(self, ftp_conn, download_directory, file_name,
                           move_directory):
        """open and read given file into create_file method,
           move file if move_directory is given"""
        with ftp_conn.open(self._source_name(download_directory, file_name),
                           "rb") as fileobj:
            data = fileobj.read()
        return self.create_file(file_name, data)

    def _source_name(self, download_directory, file_name):
        """helper to get the full name"""
        return download_directory + '/' + file_name

    def _move_file(self, ftp_conn, source, target):
        """Moves a file on the FTP server"""
        _logger.info('Moving file %s %s' % (source, target))
        ftp_conn.rename(source, target)

    def _delete_file(self, ftp_conn, source):
        """Deletes a file from the FTP server"""
        _logger.info('Deleting file %s' % source)
        ftp_conn.remove(source)

    def run(self):
        port_session_factory = ftputil.session.session_factory(
            port=self.port)
        with ftputil.FTPHost(self.host, self.user,
                             self.pwd,
                             session_factory=port_session_factory) as ftp_conn:

            file_list = ftp_conn.listdir(self.path)
            downloaded_files = []
            for ftpfile in file_list:
                source_name = self._source_name(self.path, self.file_name)
                if ftp_conn.path.isfile(source_name) and \
                        ftpfile == self.file_name:
                    self._handle_new_source(
                            ftp_conn,
                            self.path,
                            self.file_name,
                            self.move_path)
                    downloaded_files.append(self.file_name)

            # Move/delete files only after all files have been processed.
            if self.delete_file:
                for ftpfile in downloaded_files:
                    self._delete_file(ftp_conn,
                                      self._source_name(self.path,
                                                        ftpfile))
            elif self.move_path:
                if not ftp_conn.path.exists(self.move_path):
                    ftp_conn.mkdir(self.move_path)
                for ftpfile in downloaded_files:
                    self._move_file(
                        ftp_conn,
                        self._source_name(self.path, ftpfile),
                        self._source_name(self.move_path, ftpfile))


class FtpExportTask(FtpTask):
    """FTP Configuration options:
     - host, user, password, port
     - upload_directory:  directory on the FTP server where files are
                          uploaded to
    """

    _synchronize_type = 'export'

    def _handle_existing_target(self, ftp_conn, target_name, filedata):
        raise Exception("%s already exists" % target_name)

    def _handle_new_target(self, ftp_conn, target_name, filedata):
        with ftp_conn.open(target_name, mode='wb') as fileobj:
            fileobj.write(filedata)
            _logger.info('wrote %s, size %d', target_name, len(filedata))
        return file_id

    def _target_name(self, ftp_conn, upload_directory, filename):
        return upload_directory + '/' + filename

    def _upload_file(self, config, filename, filedata):
        ftp_config = config['ftp']
        upload_directory = ftp_config.get('upload_directory', '')
        port_session_factory = ftputil.session.session_factory(
            port=int(ftp_config.get('port', 21))
            )
        with ftputil.FTPHost(ftp_config['host'], ftp_config['user'],
                             ftp_config['password'],
                             session_factory=port_session_factory) as ftp_conn:
            target_name = self._target_name(ftp_conn,
                                            upload_directory,
                                            filename)
            if ftp_conn.path.isfile(target_name):
                self._handle_existing_target(ftp_conn, target_name, filedata)
            else:
                self._handle_new_target(ftp_conn, target_name, filedata)

    def run(self, config=None, file_id=None, async=True):
        #TODO change when object was made
        f = self.env.get('impexp.file') \
                .browse(self.env.cr, self.env.uid, file_id)
        self._upload_file(config, f.attachment_id.datas_fname,
                          b64decode(f.attachment_id.datas))

