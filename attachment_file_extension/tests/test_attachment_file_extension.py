import hashlib
import os
from openerp.tests.common import TransactionCase

HASH_SPLIT = 2


class TestAttachmentFileEstension(TransactionCase):

    def setUp(self):
        super(TestAttachmentFileEstension, self).setUp()
        registry, cr, uid = self.registry, self.cr, self.uid
        self.ira = registry('ir.attachment')
        self.filestore = self.ira._filestore(cr, uid)

        # Blob
        self.blob = 'blob'
        self.blob_b64 = self.blob.encode('base64')
        blob_hash = hashlib.sha1(self.blob).hexdigest()
        self.blob_fname = blob_hash[:HASH_SPLIT] + '/' + blob_hash
        self.blob_datas_fname = 'ira.ext'

    def test_01_store_on_disk(self):
        cr, uid = self.cr, self.uid

        ira_id = self.ira.create(
            cr, uid, {'name': 'ira',
                      'datas': self.blob_b64,
                      'datas_fname': self.blob_datas_fname})
        attachment = self.ira.browse(cr, uid, ira_id)
        filename, extension = os.path.splitext(self.blob_datas_fname)

        self.assertEqual(attachment.store_fname, self.blob_fname)
        self.assertEqual(attachment.extension, extension)
        self.assertTrue(
            os.path.isfile(os.path.join(
                self.filestore,
                attachment.store_fname + attachment.extension)))
