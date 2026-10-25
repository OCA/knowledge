import hashlib
import logging
import re
from pathlib import Path

from lxml import html as lhtml
from markupsafe import Markup

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.fields import Domain
from odoo.modules.module import get_module_path
from odoo.tools import plaintext2html
from odoo.tools.sql import column_exists

_logger = logging.getLogger(__name__)

try:
    import markdown
except ImportError:
    _logger.debug("markdown not installed")

LANG_RE = re.compile(r"^[a-z]{2,3}_[A-Z]{2}(@\w+)?$")
FRONT_MATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)


class HelpSection(models.Model):
    """Part of the help of a screen: written in Odoo or shipped by a module
    as Markdown files (see `_load_markdown`).

    A section targets either a window action, or a model: then it is shown on
    every screen of this model, whatever the action."""

    _name = "help.section"
    _description = "Help Section"
    _order = "sequence, id"

    action_id = fields.Many2one("ir.actions.act_window", ondelete="cascade", index=True)
    model_id = fields.Many2one(
        "ir.model",
        ondelete="cascade",
        help="Shown on every screen of this model, whatever the action.",
    )
    model = fields.Char(
        string="Model Name", related="model_id.model", store=True, index=True
    )
    sequence = fields.Integer(default=10)
    module = fields.Char(
        readonly=True, help="Module shipping this section: removed with it."
    )
    lang = fields.Selection(
        selection="_get_langs", help="Empty: shown whatever the user language."
    )
    content = fields.Html()
    file = fields.Char(
        readonly=True, help="Markdown file of the module the section comes from."
    )
    checksum = fields.Char(
        readonly=True, help="Checksum of the Markdown file the section comes from."
    )

    _file_fields = ("action_id", "model_id", "lang", "content")

    def _compute_display_name(self):
        for rec in self:
            if rec.action_id:
                main = rec.action_id.name
            else:
                main = rec.model_id.name
            rec.display_name = f"{main} - {rec.module}"

    @api.constrains("action_id", "model_id")
    def _check_target(self):
        for rec in self:
            if bool(rec.action_id) == bool(rec.model_id):
                raise ValidationError(
                    self.env._("A help section targets either an action or a model.")
                )

    def write(self, vals):
        # install_mode: help files and xml data files of the modules
        if (
            not self.env.context.get("install_mode")
            and set(vals) & set(self._file_fields)
            and any(self.mapped("file"))
        ):
            raise UserError(
                self.env._(
                    "This help comes from a file of a module: edit the file "
                    "instead, its content would overwrite your changes."
                )
            )
        return super().write(vals)

    @api.model
    def _get_langs(self):
        return self.env["res.lang"].get_installed()

    @api.model
    def _for(self, action=None, model=None):
        """Sections shown on a screen: those of its action and of its model,
        in the user language"""
        targets = []
        if action:
            targets.append(Domain("action_id", "=", action.id))
        if model or action:
            targets.append(Domain("model", "=", model or action.res_model))
        if not targets:
            return self.browse()
        return self.search(
            Domain("lang", "in", (False, self.env.lang))
            & Domain("content", "!=", False)
            & Domain.OR(targets)
        )

    def _html(self, prefix):
        """Html of the sections, with an anchor on their headings,
        and its table of contents: [(level, anchor, title)]"""
        content = "".join(self.mapped("content"))
        if not content:
            return Markup(), []
        root = lhtml.fragment_fromstring(content, create_parent="div")
        toc = []
        for index, heading in enumerate(root.iter("h1", "h2", "h3")):
            anchor = f"{prefix}_{index}"
            heading.set("id", anchor)
            toc.append((int(heading.tag[1]), anchor, heading.text_content().strip()))
        return Markup(lhtml.tostring(root, encoding="unicode")), toc

    @api.model
    def get_help(self, action_id, model=None):
        """Called by the help buttons of the control panel"""
        action = self.env["ir.actions.act_window"].browse(action_id or []).exists()
        return {
            "has_help": bool(self._for(action, model)),
            "can_edit": self.env.user.has_group("screen_help.group_editor"),
        }

    @api.model
    def _load_markdown(self, module, folder="help"):
        """Load the Markdown files of the <folder> directory of a module:

        - <model>[.<lang>].md: help of every screen of the model,
          e.g. help/sale.order.md
        - <action xmlid>[.<lang>].md: help of a window action,
          e.g. help/sale.action_quotations.fr_FR.md

        Optional header at the top of the file, to order the sections:
            ---
            sequence: 20
            ---

        Called for each installed / updated module (see ir.model.data):
        the module doesn't need to depend on screen_help.
        These sections can't be edited in Odoo: their file is the reference.
        The sections are removed with the module."""
        module_path = get_module_path(module, display_warning=False)
        path = module_path and Path(module_path, folder)
        if not path or not path.is_dir():
            return self.browse()
        langs = dict(self._get_langs())
        records = []
        for file in sorted(path.glob("*.md")):
            name, lang = file.stem, False
            prefix, __, suffix = name.rpartition(".")
            if LANG_RE.match(suffix):
                name, lang = prefix, suffix
            if lang and lang not in langs:
                continue
            values = {
                "module": module,
                "lang": lang,
                "file": str(file.relative_to(module_path)),
            }
            if name in self.env:
                values["model_id"] = self.env["ir.model"]._get_id(name)
            else:
                action = self.env.ref(name, raise_if_not_found=False)
                if action is None or action._name != "ir.actions.act_window":
                    _logger.warning("%s: unknown model or window action", file)
                    continue
                values["action_id"] = action.id
            text = file.read_text()
            checksum = hashlib.sha1(text.encode()).hexdigest()
            xml_id = "{}.help_{}".format(module, file.stem.replace(".", "_"))
            current = self.env.ref(xml_id, raise_if_not_found=False)
            if current is None or current.checksum != checksum:
                header, text = self._front_matter(text)
                values.update(content=self._md_to_html(text), checksum=checksum)
                if header.get("sequence", "").lstrip("-").isdigit():
                    values["sequence"] = int(header["sequence"])
            records.append({"xml_id": xml_id, "values": values})
        return self.with_context(
            install_mode=True, install_module=module
        )._load_records(records, update=True)

    @api.model
    def _import_help_popup(self):
        """Sections from the help of the actions of help_popup (OCA/web 8.0),
        whose columns are left in the database: `enduser_help` (html) and
        `advanced_help` (text, often html).

        Called when screen_help is installed, or updated from help_popup
        renamed to screen_help. The actions which already have a section
        written in Odoo (or imported) are skipped; the columns are kept."""
        cr = self.env.cr
        columns = [
            col
            for col in ("enduser_help", "advanced_help")
            if column_exists(cr, "ir_act_window", col)
        ]
        if not columns:
            return self.browse()
        where = " OR ".join(f"COALESCE({col}, '') != ''" for col in columns)
        query = f"SELECT id, {', '.join(columns)} FROM ir_act_window WHERE {where}"
        done = set(self.search([("file", "=", False)]).action_id.ids)
        cr.execute(query)  # pylint: disable=sql-injection
        vals_list = []
        for row in cr.dictfetchall():
            if row["id"] in done:
                continue
            if row.get("enduser_help"):
                vals_list.append(
                    {"action_id": row["id"], "content": row["enduser_help"]}
                )
            if row.get("advanced_help"):
                text = row["advanced_help"]
                body = Markup(text) if "<" in text else plaintext2html(text)
                title = self.env._("Advanced Help")
                vals_list.append(
                    {
                        "action_id": row["id"],
                        "sequence": 20,
                        "content": Markup("<h2>%s</h2>%s") % (title, body),
                    }
                )
        _logger.info("help_popup: %s help sections imported", len(vals_list))
        return self.create(vals_list)

    @api.model
    def _front_matter(self, text):
        """Split a Markdown file into its header ({key: value}) and its content"""
        match = FRONT_MATTER_RE.match(text)
        if not match:
            return {}, text
        header = {}
        for line in match.group(1).splitlines():
            key, sep, value = line.partition(":")
            if sep:
                header[key.strip()] = value.strip()
        return header, text[match.end() :]

    @api.model
    def _md_to_html(self, text):
        return markdown.markdown(text, extensions=["tables", "fenced_code"])
