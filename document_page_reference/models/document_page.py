# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import _, api, fields, models, tools
from odoo.exceptions import ValidationError
from odoo.tools.misc import html_escape

_logger = logging.getLogger(__name__)

try:
    from jinja2.sandbox import SandboxedEnvironment
    from jinja2 import Undefined
    from jinja2.lexer import name_re as old_name_re
    import re

    name_re = re.compile(u"^%s$" % old_name_re.pattern)

    class Context(SandboxedEnvironment.context_class):
        def resolve(self, key):
            res = super().resolve(key)
            if not isinstance(res, Undefined):
                return res
            return self.parent["ref"](key)

    class Environment(SandboxedEnvironment):
        context_class = Context

    mako_template_env = Environment(
        block_start_string="<%",
        block_end_string="%>",
        variable_start_string="${",
        variable_end_string="}",
        comment_start_string="<%doc>",
        comment_end_string="</%doc>",
        line_statement_prefix="%",
        line_comment_prefix="##",
        trim_blocks=True,  # do not output newline after blocks
        autoescape=False,
    )
except Exception:
    _logger.error("Jinja2 is not available")


class DocumentPage(models.Model):

    _inherit = "document.page"

    reference = fields.Char(
        help="Used to find the document, it can contain letters, numbers and _"
    )
    content_parsed = fields.Html(compute="_compute_content_parsed")

    def get_formview_action(self, access_uid=None):
        res = super().get_formview_action(access_uid)
        view_id = self.env.ref("document_page.view_wiki_form").id
        res["views"] = [(view_id, "form")]
        return res

    @api.depends("history_head")
    def _compute_content_parsed(self):
        for record in self:
            record.content_parsed = record.get_content()

    @api.constrains("reference")
    def _check_reference(self):
        for record in self:
            if not record.reference:
                continue
            if not name_re.match(record.reference):
                raise ValidationError(_("Reference is not valid"))
            if self.search(
                [("reference", "=", record.reference), ("id", "!=", record.id)]
            ):
                raise ValidationError(_("Reference must be unique"))

    def _get_document(self, code):
        # Hook created in order to add check on other models
        document = self.search([("reference", "=", code)])
        if document:
            return document
        else:
            return self.env[self._name]

    def get_reference(self, code):
        element = self._get_document(code)
        if self.env.context.get("raw_reference", False):
            return html_escape(element.display_name)
        text = """<a href="#" class="oe_direct_line"
        data-oe-model="%s" data-oe-id="%s" name="%s">%s</a>
        """
        if not element:
            text = "<i>%s</i>" % text
        res = text % (
            element._name,
            element and element.id or "",
            code,
            html_escape(element.display_name or code),
        )
        return res

    def _get_template_variables(self):
        return {"ref": self.get_reference}

    def get_content(self):
        try:
            content = self.content
            mako_env = mako_template_env
            template = mako_env.from_string(tools.ustr(content))
            return template.render(self._get_template_variables())
        except Exception:
            _logger.error("Template from page %s cannot be processed" % self.id)
            return self.content

    def get_raw_content(self):
        return self.with_context(raw_reference=True).get_content()
