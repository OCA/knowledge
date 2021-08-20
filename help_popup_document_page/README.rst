.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

=======================
Document pages for help
=======================

This module knits ``document_page`` and ``help_popup`` together such that you can write your help texts as document pages. The advantage is that you can use your help texts also as (part of) a functional description of your installation, or the other way around.

Installation
============

To install this module, you need to:

#. install ``help_popup`` from the ``web`` repository

Configuration
=============

To configure this module, you need to:

#. add users to the `Documentation writer` or `Advanced documentation writer` group
#. if you're so inclined, provide a template in the document category `Documentation` (added by this module)

Usage
=====

Members of the above mentioned groups will have access to the the fields `Documentation for` and `Advanced documentation for` on a document page *if* the page's category is `Documentation`. In those fields, assign the window action(s) for which the current document page is the (advanced) documentation.

Given you can add multiple document pages as help for the same action (they will be concatenated), you can share writing documentation between multiple people writing about different aspects.

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
    :alt: Try me on Runbot
    :target: https://runbot.odoo-community.org/runbot/118/8.0

Known issues / Roadmap
======================

* it would be nice to have this refer to actions instead of window actions, but that's more a matter of help_popup

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
