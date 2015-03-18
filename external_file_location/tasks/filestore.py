# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 initOS GmbH & Co. KG (<http://www.initos.com>).
#    @author Valentin CHEMIERE <valentin.chemiere@akretion.com>
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

from .abstract_fs import AbstractFSTask
from base64 import b64decode
from fs.osfs import OSFS
import logging
_logger = logging.getLogger(__name__)


class FileStoreTask(AbstractFSTask):

    _key = 'filestore'
    _name = 'File Store'
    _synchronize_type = None
    _default_port = None


class FileStoreImportTask(FileStoreTask):
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

    def run(self):
        with OSFS(self.host) as fs_conn:
            files_to_process = self._get_files(fs_conn, self.path)
            for file_to_process in files_to_process:
                self._process_file(fs_conn, file_to_process)


class FileStoreExportTask(FileStoreTask):
    """FTP Configuration options:
     - host, user, password, port
     - upload_directory:  directory on the FTP server where files are
                          uploaded to
    """

    _synchronize_type = 'export'

    def run(self, async=True):
        for attachment in self.attachment_ids:
            if attachment.state in ('pending', 'failed'):
                self.attachment_id = attachment
                with OSFS(self.host) as fs_conn:
                    self._upload_file(fs_conn,
                                      self.host,
                                      self.port,
                                      self.user,
                                      self.pwd,
                                      self.path,
                                      attachment.datas_fname,
                                      b64decode(attachment.datas))
