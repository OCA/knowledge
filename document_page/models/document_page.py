# Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class DocumentPage(models.Model):
    """This class is use to manage Document."""

    _name = "document.page"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Document Page"
    _parent_name = "parent_id"
    _parent_store = True
    _rec_name = "complete_name"
    _order = "type, sequence, complete_name"

    name = fields.Char("Title", required=True)
    type = fields.Selection(
        [("content", "Content"), ("category", "Category")],
        "Type",
        help="Page type",
        default="content",
    )
    active = fields.Boolean(default=True)
    parent_id = fields.Many2one(
        "document.page", "Category", domain=[("type", "=", "category")]
    )
    child_ids = fields.One2many("document.page", "parent_id", "Children")
    content = fields.Text(
        "Content",
        compute="_compute_content",
        inverse="_inverse_content",
        search="_search_content",
        required=True,
        copy=True,
    )

    # no-op computed field
    draft_name = fields.Char(
        string="Name",
        help="Name for the changes made",
        compute=lambda x: x,
        inverse=lambda x: x,
    )

    # no-op computed field
    draft_summary = fields.Char(
        string="Summary",
        help="Describe the changes made",
        compute=lambda x: x,
        inverse=lambda x: x,
    )

    template = fields.Html(
        "Template",
        help="Template that will be used as a content template "
        "for all new page of this category.",
    )
    history_head = fields.Many2one(
        "document.page.history",
        "HEAD",
        compute="_compute_history_head",
        store=True,
        auto_join=True,
    )
    history_ids = fields.One2many(
        "document.page.history",
        "page_id",
        "History",
        order="create_date DESC",
        readonly=True,
    )
    menu_id = fields.Many2one("ir.ui.menu", "Menu", readonly=True,)
    content_date = fields.Datetime(
        "Last Contribution Date",
        related="history_head.create_date",
        store=True,
        index=True,
        readonly=True,
    )
    content_uid = fields.Many2one(
        "res.users",
        "Last Contributor",
        related="history_head.create_uid",
        store=True,
        index=True,
        readonly=True,
    )
    company_id = fields.Many2one(
        "res.company",
        "Company",
        help="If set, page is accessible only from this company",
        index=True,
        ondelete="cascade",
    )
    backend_url = fields.Char(
        string="Backend URL",
        help="Use it to link resources univocally",
        compute="_compute_backend_url",
    )

    sequence = fields.Integer(
        string="Sequence", default=10, help="Used to organise the category."
    )

    parent_path = fields.Char(index=True)
    complete_name = fields.Char(
        "Complete Name", compute="_compute_complete_name", store=True
    )

    image = fields.Binary("Image", attachment=True,)

    color = fields.Integer(string="Color Index")

    @api.multi
    def write(self, vals):
        child_ids = self
        if vals.get("color", False) and len(vals) == 1:
            child_ids = self.search(
                [("type", "=", "category"),
                 ("parent_id", "child_of", self.ids)]
            )
        res = super(DocumentPage, child_ids).write(vals)
        return res

    @api.depends("name", "parent_id.complete_name")
    def _compute_complete_name(self):
        for category in self:
            if category.parent_id:
                category.complete_name = "{} / {}".format(
                    category.parent_id.complete_name, category.name,
                )
            else:
                category.complete_name = category.name

    @api.depends("menu_id", "parent_id.menu_id")
    def _compute_backend_url(self):
        tmpl = "/web#id={}&model=document.page&view_type=form"
        for rec in self:
            url = tmpl.format(rec.id)
            # retrieve action
            action = None
            parent = rec
            while not action and parent:
                action = parent.menu_id.action
                parent = parent.parent_id
            if action:
                url += "&action={}".format(action.id)
            rec.backend_url = url

    @api.constrains("parent_id")
    def _check_parent_id(self):
        if not self._check_recursion():
            raise ValidationError(_("You cannot create recursive categories."))

    @api.multi
    def _get_page_index(self, link=True):
        """Return the index of a document."""
        self.ensure_one()
        index = []
        for subpage in self.child_ids:
            index += ["<li>" + subpage._get_page_index() + "</li>"]
        r = ""
        if link:
            r = '<a href="{}">{}</a>'.format(self.backend_url, self.name)
        if index:
            r += "<ul>" + "".join(index) + "</ul>"
        return r

    @api.multi
    @api.depends("history_head")
    def _compute_content(self):
        for rec in self:
            if rec.type == "category":
                rec.content = rec._get_page_index(link=False)
            else:
                if rec.history_head:
                    rec.content = rec.history_head.content
                else:
                    # html widget's default, so it doesn't trigger ghost save
                    rec.content = "<p><br></p>"

    @api.multi
    def _inverse_content(self):
        for rec in self:
            if rec.type == "content" \
                    and rec.content != rec.history_head.content:
                rec._create_history(
                    {
                        "name": rec.draft_name,
                        "summary": rec.draft_summary,
                        "content": rec.content,
                    }
                )

    @api.multi
    def _search_content(self, operator, value):
        return [("history_head.content", operator, value)]

    @api.multi
    @api.depends("history_ids")
    def _compute_history_head(self):
        for rec in self:
            if rec.history_ids:
                rec.history_head = rec.history_ids[0]

    @api.multi
    def _create_history(self, vals):
        self.ensure_one()
        history = self.env["document.page.history"]
        vals["page_id"] = self.id
        return history.create(vals)

    @api.onchange("parent_id")
    def _onchange_parent_id(self):
        """We Set it the right content to the new parent."""
        if not self.content or self.content == "<p><br></p>":
            if self.parent_id and self.parent_id.type == "category":
                self.content = self.parent_id.template

    @api.multi
    def unlink(self):
        menus = self.mapped("menu_id")
        res = super().unlink()
        menus.unlink()
        return res
