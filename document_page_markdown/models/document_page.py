# Copyright 2026 Escodoo
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import markdown

from odoo import api, models


class DocumentPage(models.Model):
    _inherit = "document.page"

    def _markdown_extensions(self):
        """Extensions passed to the renderer. Override to add your own."""
        return ["extra", "sane_lists", "nl2br", "admonition"]

    @api.model
    def render_markdown(self, source):
        """Render a Markdown source into the HTML inserted in a page."""
        if not source:
            return ""
        return markdown.markdown(source, extensions=self._markdown_extensions())
