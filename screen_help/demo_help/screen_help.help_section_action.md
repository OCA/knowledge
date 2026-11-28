---
sequence: 5
---

## Help shipped by a module

The sections with a _File_ come from the Markdown files of a module, in its `help`
directory:

```
my_module/help/res.partner.md                     # every screen of the model
my_module/help/base.action_partner_form.md        # one window action (xml id)
my_module/help/base.action_partner_form.fr_FR.md  # French users only
```

### Life cycle

- loaded at each installation or update of the module, which doesn't need to depend on
  _Screen Help_
- read-only here, only the sequence can be changed: edit the file instead
- a file removed from the module removes its section at the next update
- removed when the module is uninstalled
- ignored when its model or action doesn't exist (module not installed)

![Section loaded from a file](/screen_help/static/description/help3.png)

### Demo

Start the tour of the features on the contacts: `/odoo/action-base.action_partner_form`.
