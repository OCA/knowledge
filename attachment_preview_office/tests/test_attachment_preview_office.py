# Copyright 2026 Jarsa
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import base64
import io
import os
import subprocess
import zipfile
from unittest.mock import MagicMock, patch

from werkzeug.wrappers import Response

from odoo.addons.base.tests.common import BaseCommon

from ..controllers.main import AttachmentPreviewOfficeController


class TestOfficeToPdfController(BaseCommon):
    """Unit tests for the LibreOffice conversion controller."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.docx_content = base64.b64encode(b"fake docx content")
        cls.attachment = cls.env["ir.attachment"].create(
            {"name": "report.docx", "datas": cls.docx_content}
        )
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
                "odoo.addons.attachment_preview_office.controllers.main.subprocess.run"
            ) as mock_run,
            patch(
                "odoo.addons.attachment_preview_office.controllers.main.open",
                create=True,
            ) as mock_open,
            patch(
                "odoo.addons.attachment_preview_office.controllers.main.os.path.exists",
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
            "odoo.addons.attachment_preview_office.controllers.main.subprocess.run",
            side_effect=FileNotFoundError,
        ):
            result = self.controller._libreoffice_to_pdf(b"content", "docx")
        self.assertIsNone(result)

    def test_libreoffice_timeout_returns_none(self):
        """Returns None on conversion timeout."""
        with patch(
            "odoo.addons.attachment_preview_office.controllers.main.subprocess.run",
            side_effect=subprocess.TimeoutExpired(cmd="libreoffice", timeout=30),
        ):
            result = self.controller._libreoffice_to_pdf(b"content", "docx")
        self.assertIsNone(result)

    def test_libreoffice_nonzero_exit_returns_none(self):
        """Returns None when LibreOffice exits with non-zero code."""
        with patch(
            "odoo.addons.attachment_preview_office.controllers.main.subprocess.run",
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
            "odoo.addons.attachment_preview_office.controllers.main.request",
            fake_request,
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
        """When the conversion pipeline yields nothing (LibreOffice missing
        and no cached copy), the route yields HTTP 503. ``_get_pdf_cached`` is
        mocked as a whole: mocking only ``_libreoffice_to_pdf`` would be flaky,
        a previous test (or run) may have left the document in the disk cache."""
        with patch(
            "odoo.addons.attachment_preview_office.controllers.main."
            "AttachmentPreviewOfficeController._get_pdf_cached",
            return_value=None,
        ):
            self.assertEqual(self._call_route().status_code, 503)

    def test_route_success(self):
        """A successful conversion streams the PDF with HTTP 200."""
        with patch(
            "odoo.addons.attachment_preview_office.controllers.main."
            "AttachmentPreviewOfficeController._libreoffice_to_pdf",
            return_value=b"%PDF-1.4 ok",
        ):
            res = self._call_route()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_data(), b"%PDF-1.4 ok")
        self.assertEqual(res.headers["Content-Type"], "application/pdf")

    def test_route_odf_extension_accepted(self):
        """ODF formats (e.g. .ods) are converted, not just OOXML."""
        ods = self.env["ir.attachment"].create(
            {"name": "sheet.ods", "datas": base64.b64encode(b"fake ods")}
        )
        with patch(
            "odoo.addons.attachment_preview_office.controllers.main."
            "AttachmentPreviewOfficeController._libreoffice_to_pdf",
            return_value=b"%PDF-1.4 ok",
        ):
            res = self._call_route(id=ods.id, filename="sheet.ods")
        self.assertEqual(res.status_code, 200)

    def test_route_macro_enabled_extension_accepted(self):
        """Macro-enabled OOXML formats (e.g. .xlsm) are converted too."""
        xlsm = self.env["ir.attachment"].create(
            {"name": "macros.xlsm", "datas": base64.b64encode(b"fake xlsm")}
        )
        with patch(
            "odoo.addons.attachment_preview_office.controllers.main."
            "AttachmentPreviewOfficeController._libreoffice_to_pdf",
            return_value=b"%PDF-1.4 ok",
        ):
            res = self._call_route(id=xlsm.id, filename="macros.xlsm")
        self.assertEqual(res.status_code, 200)

    def test_route_non_binary_field_rejected(self):
        """A non-binary field name yields HTTP 400 (no arbitrary field read)."""
        self.assertEqual(self._call_route(field="name").status_code, 400)

    def test_route_unknown_field_rejected(self):
        """An unknown field name yields HTTP 400."""
        self.assertEqual(self._call_route(field="does_not_exist").status_code, 400)

    def test_route_oversized_rejected(self):
        """Documents over the size cap are rejected with HTTP 413."""
        from ..controllers import main as ctrl

        big = self.env["ir.attachment"].create(
            {
                "name": "big.docx",
                "datas": base64.b64encode(b"x" * 16),
            }
        )
        with patch.object(ctrl, "MAX_CONTENT_BYTES", 8):
            res = self._call_route(id=big.id, filename="big.docx")
        self.assertEqual(res.status_code, 413)

    def test_office_preview_available_flag(self):
        """The session flag reflects whether the libreoffice binary exists."""
        IrHttp = self.env["ir.http"]
        with patch(
            "odoo.addons.attachment_preview_office.models.ir_http.shutil.which",
            return_value="/usr/bin/libreoffice",
        ):
            self.assertTrue(IrHttp._attachment_preview_office_available())
        with patch(
            "odoo.addons.attachment_preview_office.models.ir_http.shutil.which",
            return_value=None,
        ):
            self.assertFalse(IrHttp._attachment_preview_office_available())

    def test_libreoffice_conversion_failure_is_logged(self):
        """A non-zero LibreOffice exit logs the captured stderr."""
        failed = self._make_fake_completed_process(returncode=1)
        failed.stderr = b"soffice: some conversion error"
        with (
            patch(
                "odoo.addons.attachment_preview_office.controllers.main."
                "subprocess.run",
                return_value=failed,
            ),
            self.assertLogs(
                "odoo.addons.attachment_preview_office.controllers.main",
                level="WARNING",
            ) as logs,
        ):
            self.assertIsNone(self.controller._libreoffice_to_pdf(b"content", "docx"))
        self.assertIn("some conversion error", logs.output[0])

    def test_spreadsheets_use_single_page_sheets_profile(self):
        """Spreadsheets seed SinglePageSheets in the LibreOffice profile
        registry (CLI JSON filter options need LO >= 7.4); other office
        formats do not."""
        captured = {}

        def fake_run(cmd, **kwargs):
            profile = next(
                str(a) for a in cmd if str(a).startswith("-env:UserInstallation=")
            ).replace("-env:UserInstallation=file://", "")
            xcu = os.path.join(profile, "user", "registrymodifications.xcu")
            captured["has_xcu"] = os.path.exists(xcu)
            if captured["has_xcu"]:
                with open(xcu, encoding="utf-8") as fh:
                    captured["xcu"] = fh.read()
            return self._make_fake_completed_process(returncode=1)

        with patch(
            "odoo.addons.attachment_preview_office.controllers.main.subprocess.run",
            side_effect=fake_run,
        ):
            self.controller._libreoffice_to_pdf(b"content", "xlsx")
            self.assertTrue(captured["has_xcu"])
            self.assertIn("SinglePageSheets", captured["xcu"])
            self.controller._libreoffice_to_pdf(b"content", "docx")
            self.assertFalse(captured["has_xcu"])

    def test_strip_saved_scroll_removes_top_left_cell(self):
        """The saved scroll position (topLeftCell) is stripped from OOXML
        worksheets so SinglePageSheets exports start at the top of the
        sheet, not at the position the file was last saved at."""
        sheet = (
            b'<worksheet><sheetViews><sheetView tabSelected="1"'
            b' topLeftCell="A55" workbookViewId="0"/></sheetViews></worksheet>'
        )
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w") as zf:
            zf.writestr("xl/workbook.xml", b"<workbook/>")
            zf.writestr("xl/worksheets/sheet1.xml", sheet)
        stripped = self.controller._strip_saved_scroll(buf.getvalue())
        with zipfile.ZipFile(io.BytesIO(stripped)) as zf:
            self.assertNotIn(b"topLeftCell", zf.read("xl/worksheets/sheet1.xml"))
            self.assertEqual(zf.read("xl/workbook.xml"), b"<workbook/>")

    def test_strip_saved_scroll_keeps_invalid_content(self):
        """Content that is not a valid zip is returned unchanged."""
        self.assertEqual(
            self.controller._strip_saved_scroll(b"not a zip"), b"not a zip"
        )

    def test_libreoffice_uses_isolated_profile(self):
        """Conversion passes an isolated UserInstallation profile to avoid the
        shared LibreOffice profile-lock collision under concurrency."""
        captured = {}

        def fake_run(cmd, **kwargs):
            captured["cmd"] = cmd
            return self._make_fake_completed_process(returncode=1)

        with patch(
            "odoo.addons.attachment_preview_office.controllers.main.subprocess.run",
            side_effect=fake_run,
        ):
            self.controller._libreoffice_to_pdf(b"content", "docx")
        self.assertTrue(
            any(str(a).startswith("-env:UserInstallation=") for a in captured["cmd"]),
            "LibreOffice must run with an isolated UserInstallation profile",
        )
