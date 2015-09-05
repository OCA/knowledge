Reindex documents
=================

This module allows you to reindex documents in case they were uploaded when the right configuration for indexation was missing.

Usage
=====

To reindex a single document, open its form and click the `Reindex document` button.

To reindex all documents, go to Settings / Configuration / Knowledge, check the box `Reindex all documents` or `Reindex all unindexed documents` and click apply. Those are done in the background, so watch your logs for the process to finish.

In a migration context, you might want to reindex all or unindexed documents. To achieve this, create a config parameter `document_reindex.reindex_unindexed_on_init` or `document_reindex.reindex_all_on_init` to have the reindexation run synchronously during installation of this module.

Credits
=======

Contributors
------------

* Holger Brunn <hbrunn@therp.nl>
* Icon courtesy of http://www.picol.org (refresh.svg) and https://github.com/odoo/odoo/blob/8.0/addons/knowledge/static/description/icon.png

Maintainer
----------

.. image:: http://odoo-community.org/logo.png
    :alt: Odoo Community Association
    :target: http://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose mission is to support the collaborative development of Odoo features and promote its widespread use.

To contribute to this module, please visit http://odoo-community.org.
