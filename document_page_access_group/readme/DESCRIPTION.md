This module allows to select which users groups have access to the
document pages.

To restrict access, the module replaces the read and edit permissions of
`document_page` (`document_page.document_page_user` and
`document_page.document_page_editor`) with its own ones and disables the
original ones, on install as well as on the upgrade to 20.0. Uninstalling the
module enables them again.
