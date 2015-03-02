# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2015 Therp BV (<http://therp.nl>).
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
{
    "name": "Move existing attachments to filesystem",
    "version": "1.0",
    "author": "Therp BV,Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "complexity": "normal",
    "description": """
Introduction
============
This addon allows to automatically move existing attachments to the file
system.

Configuration
=============
If it doesn't exist, the module creates a parameter `ir_attachment.location`
with value `file:///filestore`. This will make new attachments end up in your
root path (the odoo configuration value `root_path`) in a subdirectory called
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
""",
    "category": "Knowledge Management",
    "depends": [
        'base',
    ],
    "data": [
        "data/ir_cron.xml",
        "data/init.xml",
    ],
    "test": [
    ],
    "auto_install": False,
    "installable": True,
    "application": False,
    "external_dependencies": {
        'python': ['dateutil', 'pytz'],
    },
}
