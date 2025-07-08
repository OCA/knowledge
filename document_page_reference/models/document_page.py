# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
import re

from jinja2.sandbox import SandboxedEnvironment
from markupsafe import Markup

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools import html_escape

_logger = logging.getLogger(__name__)
env = SandboxedEnvironment(autoescape=False)


class DocumentPage(models.Model):
    _inherit = "document.page"
    _description = "Document Page"

    reference = fields.Char(
        help="Used to find the document, it can contain letters, numbers and _"
    )
    content_parsed = fields.Html(
        "Parsed Content", compute="_compute_content_parsed", sanitize=False, store=True
    )

    def get_formview_action(self, access_uid=None):
        res = super().get_formview_action(access_uid)
        view_id = self.env.ref("document_page.view_wiki_form").id
        res["views"] = [(view_id, "form")]
        return res

    @api.depends("content")
    def _compute_content_parsed(self):
        for record in self:
            try:
                raw = record.content or ""
                converted = re.sub(r"\$\{([\w_]+)\}", r"{{ resolve('\1') }}", raw)
                template = env.from_string(converted)
                rendered = template.render(resolve=record._resolve_reference)
                record.content_parsed = rendered
            except Exception as e:
                _logger.info("Render failed for %s: %s", record.id, e)
                record.content_parsed = record.content or ""

    @api.constrains("reference")
    def _check_reference_validity(self):
        for rec in self:
            if not rec.reference:
                continue
            regex = r"^[a-zA-Z_][a-zA-Z0-9_]*$"
            if not re.match(regex, rec.reference):
                raise ValidationError(_("Reference is not valid"))
            domain = [("reference", "=", rec.reference), ("id", "!=", rec.id)]
            if self.search(domain):
                raise ValidationError(_("Reference must be unique"))

    def _get_document(self, code):
        return self.search([("reference", "=", code)], limit=1)

    def get_content(self):
        for record in self:
            try:
                raw = record.content or ""
                converted = re.sub(r"\$\{([\w_]+)\}", r"{{ resolve('\1') }}", raw)
                template = env.from_string(converted)
                return template.render(resolve=record._resolve_reference)
            except Exception:
                _logger.error(
                    "Template from page with id = %s cannot be processed", record.id
                )
                return record.content

    def _resolve_reference(self, code):
        doc = self._get_document(code)
        if self.env.context.get("raw_reference", False):
            return html_escape(doc.display_name if doc else code)
        sanitized_code = html_escape(code)
        if not doc:
            return (
                f"<i><a href='#' class='oe_direct_line' "
                f"data-oe-model='document.page' data-oe-id='' "
                f"name='{sanitized_code}'>{sanitized_code}</a></i>"
            )
        return (
            f"<a href='#' class='oe_direct_line' data-oe-model='{doc._name}' "
            f"data-oe-id='{doc.id}' name='{sanitized_code}'>"
            f"{html_escape(doc.display_name)}</a>"
        )

    def get_raw_content(self):
        return Markup(self.with_context(raw_reference=True).get_content())

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get("reference") and vals.get("name"):
                reference = self.env["ir.http"]._slugify(vals["name"]).replace("-", "_")
                vals["reference"] = reference
        return super().create(vals_list)
