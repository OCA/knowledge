# Copyright 2023 len-foss/Financial Way
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import base64

from odoo.addons.attachment_indexation_ocr.tests.common import TestOcrCase
from odoo.addons.queue_job.tests.common import trap_jobs


class TestOcrJob(TestOcrCase):
    def test_document_ocr_png(self):
        vals = {"name": "testattachment", "datas": base64.b64encode(self.data_png)}
        with trap_jobs() as trap:
            attachment = self.env["ir.attachment"].create(vals)
            trap.assert_jobs_count(1)
            expected_job_desc = "Perform OCR on attachment testattachment"
            trap.assert_enqueued_job(
                self.env["ir.attachment"].perform_ocr,
                args=(),
                kwargs={},
                properties={"channel": "ocr", "description": expected_job_desc},
            )
            # the ocr has not been performed yet
            self.assertEqual(attachment.index_content.strip(), self.marker)
