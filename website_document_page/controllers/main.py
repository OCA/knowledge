# Copyright (C) 20020 Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import http
from odoo.http import request


class WikiController(http.Controller):
    @http.route(
        [
            """/wiki""",
            """/wiki/page/<model('document.page'):page>""",
            """/wiki/category/<model('document.page'):category>""",
            """/wiki/tag/<model('document.tag'):tag>""",
        ],
        type="http",
        auth="public",
        website=True,
    )
    def wiki(self, page=None, category=None, tag=None, search=""):
        Page = request.env["document.page"]
        Tag = request.env["document.tag"]
        pages = {}
        page_tags = {}

        # Page
        if not page and not category and not tag and not search:
            website = request.env["website"].get_current_website()
            page_id = website.wiki_id.id or False
            page = Page.browse(page_id)
        # Page Tags
        if page:
            page_tags = page.tag_ids
        # Category
        if category:
            pages = Page.search([("parent_id", "=", category.id)])
        # Tag
        if tag:
            pages = Page.search([("tag_ids", "in", tag.id)])
        # Search
        if search:
            pages = Page.search(
                ["|", ("name", "like", search), ("content", "like", search)]
            )
        search_count = len(pages)
        # Menu
        menu_categories = Page.search(
            [("parent_id", "=", False), ("is_menu", "=", True)]
        )
        menu_pages = Page.search([("parent_id", "!=", False), ("is_menu", "=", True)])
        menu_tags = Tag.search([("is_menu", "=", True)])

        values = {
            "category": category,
            "pages": pages,
            "page": page,
            "page_tags": page_tags,
            "tag": tag,
            "search": search,
            "search_count": search_count,
            "menu_categories": menu_categories,
            "menu_pages": menu_pages,
            "menu_tags": menu_tags,
        }
        return request.render("website_document_page.wiki", values)
