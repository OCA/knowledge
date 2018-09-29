.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

===============================
Force enable attachments upload
===============================

In odoo, by default, you can't add attachments to a record if the form view
is set as not editable (``edit='false'`` in the form tag)

This module adds a new form view attribute, ``attach=``, which lets you
enable attachment uploads even in non-editable forms.

Keep in mind: users still won't be able to attach documents
to records they don't have write access to (according to ACL and record rules);
this module does not bypass odoo' security rules!

Usage
=====

Add the ``attach="true"`` attribute to the form view tag which of uneditable views
(normal editable views already allow attaching a document and there is no need
for this attribute).

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/118/10.0


Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/OCA/
knowledge/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us smashing it by providing a detailed and welcomed feedback `here <https://github.com/OCA/
knowledge/issues/new?body=module:%20
attachment_force_attach%0Aversion:%20
10.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.


Credits
=======

Contributors
------------

* Leonardo Donelli @ MONK Software (leonardo.donelli@monksoftware.it)

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
