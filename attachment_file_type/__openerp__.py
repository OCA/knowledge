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
    "name": "File types for attachments",
    "version": "1.0",
    "author": "Therp BV,Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "description": """
File types for attachments
==========================
Adds a content type to attachments. This is useful for instance in combination
with http://bazaar.launchpad.net/~ocb/ocb-web/6.1/revision/2524, which makes
Odoo offer downloads with the correct file type based on this field.

The document module makes this field available as well. This module does not
interfere with its functionality when both are installed.

Installation
============
To install this module, you need to install python-magic in your environment
first.

Configuration
=============
This module comes with a daily scheduled task to provide content types for
attachments without one in small batches (instead of trying to do this for all
attachments at installation time). Depending on the number of attachments in
your system you may deactivate this task after some time. You can follow the
progress in the logs at the time that the cron job is fired.

Credits
=======
Contributors
------------

* Stefan Rijnhart <stefan@therp.nl>
* Holger Brunn <hbrunn@therp.nl>

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
    "depends": ['base'],
    "data": ['data/ir_cron.xml'],
    "license": 'AGPL-3',
    "external_dependencies": {
        'python': ['magic'],
    },
}
