- Users of the *Help Editor* group (and administrators) can write the help:
  *Settings > Technical > User Interface > Help Sections*, or the *Edit*
  button of the help window.
- *Settings > General Settings > Help > Multilingual Help*: a section can be
  written for a given language. A section without language is shown to
  everybody. The help is not translated through the standard translation
  mechanism.
- Dark mode: the help window follows the color scheme of the user
  (`ir.http.color_scheme()`) when a module provides it, e.g. `web_dark_mode`
  (OCA/web) or `web_enterprise`; no dependency on them.
