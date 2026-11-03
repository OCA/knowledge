Office-document preview (DOCX, XLSX, PPTX, ODT, ODS, ODP, and legacy formats)
requires **LibreOffice** to be installed on the Odoo server — it is used in
headless mode to convert documents to PDF. It is *not* part of the standard Odoo
image, so install it on the host/container running Odoo:

    sudo apt-get install libreoffice

Without LibreOffice the office-preview endpoint returns HTTP 503 and only PDF
files can be previewed. PDF preview needs no extra packages.

For best filetype recognition, also install `python-magic`:

    sudo apt-get install python-magic
