.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

====
SFTP
====

This module allows you to access your data (= documents attached to records)
via SFTP. There will be different virtual roots to get your browsing started,
for the time being, there's only one map `By model` that lets you browse ids
of the records of the different models.

Installation
============

To install this module, you need to:

#. install paramiko. You need version 2.0 or higher
#. install the module. It will generate a new host key during installation

Configuration
=============

To configure this module, you need to:

#. be sure there's a proper hostkey in config parameter ``document_sftp.hostkey``
#. add some authorized key on the users' form who should be allowed to login via SFTP

Usage
=====

To use this module, you need to:

#. add some keys to your user's authorized key field
#. say ``sftp -p 2222 $yourodoohost`` and browse through the possibilities
#. when you found what you want, say ``sshfs -p 2222 "admin@localhost:By model/res.company/1" $yourmountpoint`` to see all attachments of your main company in ``$yourmountpoint``
#. pay someone to implement locking (see below) in order to be able to write on this

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
    :alt: Try me on Runbot
    :target: https://runbot.odoo-community.org/runbot/118/8.0

Known issues / Roadmap
======================

* implement writing. This is not trivial, because we need some concept of locking, UI for that and take care of some corner cases
* allow to restrict actions on SFTP that are allowed normally (because ``rf -rf $yourmountpoint/`` can become a serious problem)
* should support directories
* implement some other useful virtual roots (Mails, By Directory, By name, ...)
  This should look like symlinks to the rigid designator (model+id) from the point of view of the user.
* with this, `auth_ssh` should be simple to implement enabling passwordless logins for your scripts
* if you want to see error messages from the SFTP server thread, use ``--log-handler=paramiko:DEBUG``

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
