LibreOffice must be installed on the Odoo server and the `libreoffice`
binary must be available in the PATH of the Odoo process:

    apt-get install libreoffice

On Odoo.sh, LibreOffice is already available by default.

If LibreOffice is not available, the module still installs, but the
preview button is simply not shown for office files (the availability is
exposed to the web client through the session info).
