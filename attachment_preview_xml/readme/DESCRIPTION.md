Preview XML attachments as a collapsible tree instead of a wall of text.

Odoo stores XML attachments with the `text/plain` mimetype for any user
without write access on views, so the standard file viewer renders them as
raw text. Machine-generated XML (electronic invoices such as CFDI or UBL,
bank statements, EDI messages) usually comes in a single line, which makes
that preview unreadable.

This module renders XML attachments with their hierarchy: indented nodes,
highlighted tags, attributes and values, and every branch can be collapsed
or expanded. Everything happens in the browser, no conversion service and no
extra software on the server.
