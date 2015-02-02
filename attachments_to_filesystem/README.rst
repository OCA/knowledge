Introduction
============
This addon allows to automatically move existing attachments to the file
system.

Configuration
=============
If it doesn't exist, the module creates a parameter `ir_attachment.location`
with value `file`. This will make new attachments end up in your
data path (the odoo configuration value `data_dir`) in a subdirectory called
`filestore`.

Then it will create a cron job that does the actual transfer and schedule it
for 01:42 at night in the installing user's time zone. The cronjob will do a
maximum of 10000 conversions per run and is run every night.
The limit is configurable with the parameter `attachments_to_filesystem.limit`.

After all attachments are migrated (the log will show then `moving 0
attachments to filestore`), you can disable or delete the cronjob.

If you need to run the migration synchronously during install, set the
parameter `attachments_to_filesystem.move_during_init` *before* installing this
addon.

Credits
=======

Contributors
------------

* Holger Brunn <hbrunn@therp.nl>

Icon
----

http://commons.wikimedia.org/wiki/File:Crystal_Clear_app_harddrive.png

Maintainer
----------

.. image:: http://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: http://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

To contribute to this module, please visit http://odoo-community.org.

