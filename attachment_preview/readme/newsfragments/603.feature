Add office-document preview (DOCX, XLSX, PPTX, legacy DOC/XLS/PPT, and ODF
formats) by converting them to PDF with LibreOffice headless and rendering the
result through Odoo's native PDF.js viewer. ViewerJS is no longer bundled. The
conversion endpoint validates the binary field, caps document size, caches
results by checksum, and runs each LibreOffice conversion with an isolated user
profile so concurrent previews do not collide. Returns HTTP 503 gracefully when
LibreOffice is not installed.
