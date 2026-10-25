**Read the help**: click the book button of the control panel. The button is
shown when the screen has some help, or to the help editors.

**Write the help in Odoo**: *Edit* button of the help window, then add a
section targeting the action or the model of the screen.

![Help window beside Odoo](../static/description/help1.png)

**Ship the help in a module**: add Markdown files in its `help` directory:

```
my_module/help/sale.order.md                     # every screen of the model
my_module/help/sale.action_quotations.md         # one window action (xml id)
my_module/help/sale.action_quotations.fr_FR.md   # in French only
```

**You don't need to depends on screen_help** to provide a such files to document your module,
 just add markdown like above

An optional header orders the sections (sequence 10 by default). In the
application help, the screens are ordered by the lowest sequence of their
sections, then by the menu order:

```markdown
---
sequence: 20
---
## My help
```

When `screen_help` is installed, the `help` directory of a module is loaded at
each installation / update of the module (and for all the installed modules at
the installation of `screen_help`). Without `screen_help`, it is ignored.

- a section loaded from a file can't be edited in Odoo
- a file removed from the module removes its section at the next update
- a file whose model or action doesn't exist (module not installed) is ignored
- the headings (`#`, `##`, `###`) make the table of contents of the help window

![Section loaded from a file](../static/description/help3.png)

**Demo**: on a database with demo data, a tour documents each feature on the
screen that shows it, each section pointing to the next screen
 like contacts, [/odoo/action-base.action_partner_form](/odoo/action-base.action_partner_form)

![Help window in dark mode](../static/description/help2.png)
