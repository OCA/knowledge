.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=============
Document Page
=============

This module allows you to write web pages for internal documentation.

Installation
============

This module depends on module knowledge. So make sure to have available it in your addons list

Configuration
=============

No configuration required

Usage
=====

To use this module, you need to:
* Go to Knowledge menu
* Click on Categories to create the document's category you need with the template
* Click on Pages to create pages and select the previous category to use the template


.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/118/9.0

Known issues / Roadmap
======================

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/OCA/
{project_repo}/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us smashing it by providing a detailed and welcomed feedback `here <https://github.com/OCA/knowledge/issues/new?body=module:%20document_page%0Aversion:%209.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.

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

v 9.0.1.0.0

Creation of folders models, views, data and demo
document_page_view.xml moved to views and renamed to document_page
document_page_data.xml moved to data and renamed to document_page
document_page_demo.xml moved to demo and renamed to document_page
document_page.py moved to models and renamed to document_page

Module models initialise by the creation of the file __init__.py

wizard file reorganized
folder wizard created
document_page_create_menu.py and document_page_create_show_diff.py moved to wizard
document_page_create_menu_view.xml moved to document_page_create_menu.xml
document_page_create_show_diff_view.xml en document_page_create_show_diff.xml


__openerp_.py et __init__.py file edited in order to reflect the module organization
