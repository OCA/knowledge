Preview office documents (DOCX, XLSX, PPTX, macro-enabled DOCM, XLSM, PPTM,
legacy DOC, XLS, PPT, and ODT, ODS, ODP, ODG) directly in the browser,
including chatter attachments.

The document is converted to PDF on the Odoo server using LibreOffice in
headless mode and rendered with Odoo's native PDF.js viewer. Nothing leaves
your server: no external viewer service (Microsoft Office Online, Google
Docs) is involved, which makes this suitable for sensitive documents.

Converted PDFs are cached on disk (keyed by document checksum), so each
document is only converted once. The *Download* button still downloads the
original file, not the converted PDF.
