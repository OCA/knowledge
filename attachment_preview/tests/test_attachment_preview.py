# Copyright 2018 Onestein
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import base64
import subprocess
from unittest.mock import MagicMock, patch

from werkzeug.wrappers import Response

from odoo.addons.base.tests.common import BaseCommon
from odoo.addons.mail.tools.discuss import Store


class TestAttachmentPreview(BaseCommon):
    def test_get_extension(self):
        attachment = self.env["ir.attachment"].create(
            {
                "datas": base64.b64encode(b"from this, to that."),
                "name": "doc.txt",
            }
        )
        attachment2 = self.env["ir.attachment"].create(
            {
                "datas": base64.b64encode(b"Png"),
                "name": "image.png",
            }
        )
        attachment3 = self.env["ir.attachment"].create(
            {
                "datas": base64.b64encode(b"Png"),
                "name": "image",
            }
        )
        res = self.env["ir.attachment"].get_attachment_extension(attachment.id)
        self.assertEqual(res, "txt")
        store = Store()
        attachment._to_store(store)
        store_data = store.get_result()
        self.assertIn("extension", store_data["ir.attachment"][0])
        res = self.env["ir.attachment"].get_attachment_extension(
            [attachment.id, attachment2.id]
        )
        self.assertEqual(res[attachment.id], "txt")
        self.assertEqual(res[attachment2.id], "png")

        res2 = self.env["ir.attachment"].get_binary_extension(
            "ir.attachment", attachment.id, "datas"
        )
        self.assertTrue(res2)

        module = (
            self.env["ir.module.module"].search([]).filtered(lambda m: m.icon_image)[0]
        )
        res3 = self.env["ir.attachment"].get_binary_extension(
            "ir.module.module", module.id, "icon_image"
        )
        self.assertTrue(res3)

        res4 = self.env["ir.attachment"].get_binary_extension(
            "ir.attachment", attachment3.id, "datas", "name"
        )
        self.assertTrue(res4)

        res5 = self.env["ir.attachment"].get_binary_extension(
            "ir.attachment", attachment.id, None
        )
        self.assertFalse(res5)

        res6 = self.env["ir.attachment"].get_binary_extension(
            "ir.attachment", attachment3.id, "datas", "dummy"
        )
        self.assertTrue(res6)


class TestOfficeToPdfController(BaseCommon):
    """Unit tests for the LibreOffice conversion controller."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.docx_content = base64.b64encode(b"fake docx content")
        cls.attachment = cls.env["ir.attachment"].create(
            {"name": "report.docx", "datas": cls.docx_content}
        )
        from ..controllers.main import AttachmentPreviewOfficeController

        cls.controller = AttachmentPreviewOfficeController()

    def _make_fake_completed_process(self, returncode=0):
        result = subprocess.CompletedProcess(args=[], returncode=returncode)
        result.stdout = b""
        result.stderr = b""
        return result

    def test_libreoffice_to_pdf_success(self):
        """Returns PDF bytes when LibreOffice succeeds."""
        fake_pdf = b"%PDF-1.4 fake"
        with (
            patch(
                "odoo.addons.attachment_preview.controllers.main.subprocess.run"
            ) as mock_run,
            patch(
                "odoo.addons.attachment_preview.controllers.main.open",
                create=True,
            ) as mock_open,
            patch(
                "odoo.addons.attachment_preview.controllers.main.os.path.exists",
                return_value=True,
            ),
        ):
            mock_run.return_value = self._make_fake_completed_process(returncode=0)
            mock_open.return_value.__enter__ = lambda s: s
            mock_open.return_value.__exit__ = lambda s, *a: False
            mock_open.return_value.read = lambda: fake_pdf
            mock_open.return_value.write = lambda data: None
            result = self.controller._libreoffice_to_pdf(b"content", "docx")
        self.assertIsNotNone(result)

    def test_libreoffice_not_installed_returns_none(self):
        """Returns None when LibreOffice binary is not found."""
        with patch(
            "odoo.addons.attachment_preview.controllers.main.subprocess.run",
            side_effect=FileNotFoundError,
        ):
            result = self.controller._libreoffice_to_pdf(b"content", "docx")
        self.assertIsNone(result)

    def test_libreoffice_timeout_returns_none(self):
        """Returns None on conversion timeout."""
        with patch(
            "odoo.addons.attachment_preview.controllers.main.subprocess.run",
            side_effect=subprocess.TimeoutExpired(cmd="libreoffice", timeout=30),
        ):
            result = self.controller._libreoffice_to_pdf(b"content", "docx")
        self.assertIsNone(result)

    def test_libreoffice_nonzero_exit_returns_none(self):
        """Returns None when LibreOffice exits with non-zero code."""
        with patch(
            "odoo.addons.attachment_preview.controllers.main.subprocess.run",
            return_value=self._make_fake_completed_process(returncode=1),
        ):
            result = self.controller._libreoffice_to_pdf(b"content", "docx")
        self.assertIsNone(result)

    # -- route handler (office_to_pdf) branch coverage -------------------------

    def _call_route(self, **over):
        """Invoke office_to_pdf with ``request`` patched to the test env;
        return the resulting werkzeug Response."""

        def make_response(data, status=200, headers=None):
            return Response(data, status=status, headers=headers or [])

        fake_request = MagicMock()
        fake_request.env = self.env
        fake_request.make_response.side_effect = make_response
        params = {
            "model": "ir.attachment",
            "field": "datas",
            "id": self.attachment.id,
            "filename": "report.docx",
        }
        params.update(over)
        with patch(
            "odoo.addons.attachment_preview.controllers.main.request", fake_request
        ):
            return self.controller.office_to_pdf(**params)

    def test_route_bad_id(self):
        """A non-integer id yields HTTP 400."""
        self.assertEqual(self._call_route(id="not-an-int").status_code, 400)

    def test_route_no_content(self):
        """A record with no binary content yields HTTP 404."""
        empty = self.env["ir.attachment"].create({"name": "empty.docx"})
        self.assertEqual(self._call_route(id=empty.id).status_code, 404)

    def test_route_unsupported_extension(self):
        """A non-Office extension yields HTTP 415."""
        self.assertEqual(self._call_route(filename="notes.txt").status_code, 415)

    def test_route_libreoffice_unavailable(self):
        """When conversion returns None, the route yields HTTP 503."""
        with patch(
            "odoo.addons.attachment_preview.controllers.main."
            "AttachmentPreviewOfficeController._libreoffice_to_pdf",
            return_value=None,
        ):
            self.assertEqual(self._call_route().status_code, 503)

    def test_route_success(self):
        """A successful conversion streams the PDF with HTTP 200."""
        with patch(
            "odoo.addons.attachment_preview.controllers.main."
            "AttachmentPreviewOfficeController._libreoffice_to_pdf",
            return_value=b"%PDF-1.4 ok",
        ):
            res = self._call_route()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_data(), b"%PDF-1.4 ok")
        self.assertEqual(res.headers["Content-Type"], "application/pdf")
