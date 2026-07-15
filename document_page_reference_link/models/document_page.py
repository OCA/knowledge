# Copyright 2019 Creu Blanca
# Copyright 2025 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import re

from markupsafe import Markup

from odoo import api, fields, models
from odoo.tools import html_escape


class DocumentPage(models.Model):
    _inherit = "document.page"
    _description = "Document Page"

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
            record.content_parsed = record.get_content()

    def _get_document(self, code):
        return self.search([("reference", "=", code)], limit=1)

    def get_content(self):
        self.ensure_one()
        raw = str(self.content or "")
        content_parsed = Markup(raw)
        for text in re.findall(r"\{\{.*?\}\}", raw):
            reference = re.sub(r"<[^>]*>", "", text).replace("{{", "").replace("}}", "")
            content_parsed = content_parsed.replace(
                text, self._resolve_reference(reference)
            )
        link_regex = (
            r"<a[^>]*class=['\"][^'\"]*oe_direct_line[^'\"]*['\"]"
            r"[^>]*name=['\"]([^'\"]*)['\"][^>]*>.*?</a>"
        )
        for match in re.finditer(link_regex, raw):
            full_link = match.group(0)
            reference = match.group(1)
            content_parsed = content_parsed.replace(
                Markup(full_link), self._resolve_reference(reference)
            )
        return content_parsed

    def _inverse_content(self):
        for rec in self:
            if rec.type == "content":
                rec.content = rec.get_content()
        return super()._inverse_content()

    def _resolve_reference(self, code):
        doc = self._get_document(code)
        if self.env.context.get("raw_reference", False):
            return html_escape(doc.display_name if doc else code)
        sanitized_code = html_escape(code)
        oe_model = doc._name if doc else self._name
        oe_id = doc.id if doc else ""
        name = html_escape(doc.display_name) if doc else sanitized_code
        href = doc.backend_url if doc else "#"
        return Markup(
            f"<a href='{href}' class='oe_direct_line' data-oe-model='{oe_model}' "
            f"data-oe-id='{oe_id}' name='{sanitized_code}'>"
            f"{name}</a>"
        )

    def get_raw_content(self):
        return Markup(self.with_context(raw_reference=True).get_content())
