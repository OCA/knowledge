.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

=================
OCR for documents
=================

This module was written to make uploaded documents, for example scans, searchable by running OCR on them.

It supports all image formats `Pillow supports <http://pillow.readthedocs.io/en/3.2.x/handbook/image-file-formats.html>`_ for reading and PDFs.

Installation
============

To install this module, you need to:

#. install tesseract and the language(s) your documents use
#. if you want to support OCR on PDFs, install imagemagick
#. install the module itself

On an Debian or Ubuntu system you would typically run::

    $ sudo apt-get install tesseract-ocr imagemagick


Configuration
=============

To configure this module, go to:

#. Settings/Technical/Parameters/System parameters and review the parameters with names document_ocr.*

Usage
=====

By default, character recognition is done asynchronously by a cronjob at night. 
This is because the recognition process takes a while and you don't want to make your users wait for the indexation to finish.
The interval to run the cronjob can be adjusted to your needs in the ``Scheduled Actions`` menu, under ` `Settings``.
In case you want to force the OCR to be done immediately, set configuration parameter ``document_ocr.synchronous`` to value ``True``.

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
    :alt: Try me on Runbot
    :target: https://runbot.odoo-community.org/runbot/118/8.0

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/OCA/knowledge/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us smashing it by providing a detailed and welcomed feedback.

Credits
=======

The actual work
---------------

* `tesseract <https://github.com/tesseract-ocr>`_

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
