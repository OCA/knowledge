.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

====
WOPI
====

This module was written to implement the `WOPI protocol <http://wopi.readthedocs.io/projects/wopirest>`_ in order to allow online collaborative editing and viewing of office files. This works with `LibreOffice online <https://wiki.documentfoundation.org/Development/LibreOffice_Online>`_/`Collabora online <https://www.collaboraoffice.com/collabora-online>`_ and probably also with Office 365.

Installation
============

To install this module, you need to:

#. have a WOPI client available. For testing, use one of the `Collabora <https://hub.docker.com/r/collabora/code>`_ or `Libreoffice <https://hub.docker.com/r/libreoffice/online/>`_ docker images. The first works out of the box, but is rate limited, the second needs manual interaction, but is unmodified. The `Nextcloud documentation <https://nextcloud.com/collaboraonline/>`_ contains some information on how to get this running
#. have your instance accessible on port 443 via your WOPI client and should have a valid SSL certificate
#. use a dbfilter if necessary to have unauthenticated requests ending up in the database you want

Configuration
=============

To configure this module, you need to:

#. fill in your WOPI client URL in the configuration wizard

Usage
=====

To use this module, you need to:

#. on any supported attachment, click the edit button

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
    :alt: Try me on Runbot
    :target: https://runbot.odoo-community.org/runbot/118/8.0

Known issues / Roadmap
======================

* implement quasi permanent public shares a la google docs
* whoever want to get their hands dirty with Microsoft should find our how to integrate this with Office 365

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/OCA/knowledge/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smashing it by providing a detailed and welcomed feedback.

Credits
=======

Images
------

* Odoo Community Association: `Icon <https://github.com/OCA/maintainer-tools/blob/master/template/module/static/description/icon.svg>`_.

Contributors
------------

* Holger Brunn <hbrunn@therp.nl>

Do not contact contributors directly about help with questions or problems concerning this addon, but use the `community mailing list <mailto:community@mail.odoo.com>`_ or the `appropriate specialized mailinglist <https://odoo-community.org/groups>`_ for help, and the bug tracker linked in `Bug Tracker`_ above for technical issues.

Maintainer
----------

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

To contribute to this module, please visit https://odoo-community.org.
