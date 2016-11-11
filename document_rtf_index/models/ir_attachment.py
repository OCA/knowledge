# -*- coding: utf-8 -*-
# © 2016 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import logging

from openerp import api, models


_logger = logging.getLogger(__name__)


class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    @api.noguess
    def _register_hook(self, cr):
        """Only register our indexer if module is installed."""
        import StringIO
        try:
            from pyth import document
            from pyth.plugins.rtf15.reader import Rtf15Reader
            from pyth.plugins.plaintext.writer import PlaintextWriter
        except ImportError:
            _logger.warn("pyth not found, RTF indexing disabled.")
            return
        from openerp.addons.document.content_index import indexer, cntIndex
        from openerp.addons.document.std_index import _to_unicode

        def improved_paragraph(self, paragraph, prefix=""):
            """Override method to insert image ignoring code."""
            content = []
            for text in paragraph.content:
                # Begin patch =========\
                if text.__class__ is document.Image:
                    continue
                # End patch ===========/
                content.append(u"".join(text.content))
            content = u"".join(content).encode("utf-8")
            for line in content.split("\n"):
                self.target.write("  " * self.indent)
                self.target.write(prefix)
                self.target.write(line)
                self.target.write("\n")
                if prefix:
                    prefix = "  "

        PlaintextWriter.paragraph = improved_paragraph

        class RtfDoc(indexer):
            """Index Rich Text Format (RTF) files."""

            def _getMimeTypes(self):
                return [
                    'application/rtf',
                    'application/x-rtf',
                    'text/rtf',
                    'text/richtext',
                ]

            def _getExtensions(self):
                return [
                    '.rtf',
                ]

            def _doIndexContent(self, content):
                """Just get text contents of rtf file."""
                s = StringIO.StringIO(content)
                r = Rtf15Reader.read(s)  # r will be pyth.document.Document
                s.close()
                w = PlaintextWriter.write(r)  # w will be cStringIO.StringO
                result = _to_unicode(w.getvalue())
                return result

        cntIndex.register(RtfDoc())
