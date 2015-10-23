.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

================================
Knowledge Management System base
================================

This module allows you to write web pages for internal documentation.

Installation
============

Makes the Knowledge Application Configuration available from where you can install
document and Wiki based Hidden.

Configuration
=============

No configuration required

Usage
=====

To use this module, you need to:


.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/{repo_id}/{branch}

.. repo_id is available in https://github.com/OCA/maintainer-tools/blob/master/tools/repos_with_ids.txt
.. branch is "8.0" for example

Known issues / Roadmap
======================

* ...

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/OCA/
{project_repo}/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us smashing it by providing a detailed and welcomed feedback `here <https://github.com/OCA/
{project_repo}/issues/new?body=module:%20
{module_name}%0Aversion:%20
{version}%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.


Credits
=======

Contributors
------------

* Odoo SA <info@odoo.com>
* Savoir-faire Linux <support@savoirfairelinux.com>
* Gervais Naoussi <gervaisnaoussi@gmail.com>

Maintainer
----------

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

To contribute to this module, please visit http://odoo-community.org.

Changelog
---------

v9.0.1.0.0

This module is an official module but was not present in odoo 9.0 official repository
so we took it from Odoo 8.0 repository and add it here.

Here are the modification that have been done to make it work

We added views folder
we moved Knowledge_view.xml and res_config_view.xml to views
we renamed Knowledge_view.xml to Knowledge.xml and res_config_view.xml to res_config.xml

res_config view is edited so that knowledge setting is accessible the following way
"knowledge/configuration/settings"

We added demo folder
we moved Knowledge_demo.xml to demo
we renamed Knowledge_demo.xml to Knowledge.xml and


we created models folder
we moved res_config.py to that folder and edited it to respect the new Odoo model api
and OCA guidelines
#osv.osv_memory replace by models.TransientModel
#_columns removed
we created the __init__.py file

we edited the __openerp__.py file to reflect the new folder structure
