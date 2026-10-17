Contextual help on the screens of Odoo, written in Odoo or shipped by modules
as Markdown files.

A book button in the control panel opens the help of the
current screen in a window detached from the Odoo tab, which can stay open
beside Odoo.

The help of a screen is made of sections, ordered by sequence, which target:

- a window action: shown on the screens of this action
- or a model: shown on every screen of this model, whatever the action

A section is either written in Odoo by the help editors (HTML editor), or
shipped by a module as a Markdown file: converted to HTML when the module is
installed or updated, read-only in Odoo, and removed with the module. The
module shipping the files doesn't need to depend on `screen_help`.
