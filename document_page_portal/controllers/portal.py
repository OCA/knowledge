# Copyright (C) 2020 - TODAY, Marcel Savegnago - Escodoo).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import http
from odoo.exceptions import AccessError, MissingError
from odoo.http import request
from odoo.tools.translate import _
from odoo.addons.portal.controllers.portal import pager as portal_pager, CustomerPortal
from odoo.osv.expression import OR


class CustomerPortal(CustomerPortal):

    def _prepare_portal_layout_values(self):
        values = super(CustomerPortal, self)._prepare_portal_layout_values()
        values['document_page_count'] = request.env[
            'document.page'].search_count([('type', '=', 'content')])
        return values

    def _document_page_get_page_view_values(self, document_page,
                                            access_token, **kwargs):
        values = {
            'page_name': 'document_page',
            'document_page': document_page,
        }
        return self._get_page_view_values(
            document_page, access_token, values,
            'my_document_pages_history', False, **kwargs)

    @http.route(
        ['/my/knowledge/documents/', '/my/knowledge/documents/page/<int:page>'],
        type='http', auth="user", website=True)
    def portal_my_knowledge_document_pages(self, page=1, date_begin=None,
                                           date_end=None, sortby=None,
                                           search=None, search_in='content', **kw):
        values = self._prepare_portal_layout_values()
        domain = [('type', '=', 'content')]

        searchbar_sortings = {
            'date': {'label': _('Newest'), 'order': 'create_date desc'},
            'name': {'label': _('Name'), 'order': 'name'},
            'parent': {'label': _('Category'), 'order': 'parent_id'},
        }
        searchbar_inputs = {
            'content': {'input': 'content', 'label': _(
                'Search <span class="nolabel"> (in Content)</span>')},
            'all': {'input': 'all', 'label': _('Search in All')},
        }

        # default sort by value
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']

        # archive groups - Default Group By 'create_date'
        archive_groups = self._get_archive_groups('document.page', domain)
        if date_begin and date_end:
            domain += [
                ('create_date', '>', date_begin),
                ('create_date', '<=', date_end),
            ]

        # search
        if search and search_in:
            search_domain = []
            if search_in in ('content', 'all'):
                search_domain = OR([search_domain, [
                    '|', ('name', 'ilike', search), ('content', 'ilike', search)]])
            domain += search_domain

        # pager
        document_pages_count = request.env['document.page'].search_count(domain)
        pager = portal_pager(
            url="/my/knowledge/documents",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
            total=document_pages_count,
            page=page,
            step=self._items_per_page
        )

        document_pages = request.env['document.page'].search(
            domain, order=order, limit=self._items_per_page, offset=pager['offset'])
        request.session['my_document_pages_history'] = document_pages.ids[:100]

        values.update({
            'date': date_begin,
            'document_pages': document_pages,
            'page_name': 'document_page',
            'default_url': '/my/knowledge/s',
            'pager': pager,
            'archive_groups': archive_groups,
            'searchbar_sortings': searchbar_sortings,
            'searchbar_inputs': searchbar_inputs,
            'sortby': sortby,
            'search_in': search_in,
            'search': search,
        })
        return request.render(
            "document_page_portal.portal_my_knowledge_document_pages", values)

    @http.route([
        "/knowledge/document/<int:document_page_id>",
        "/knowledge/document/<int:document_page_id>/<token>",
        '/my/knowledge/document/<int:document_page_id>'
    ], type='http', auth="public", website=True)
    def document_pages_followup(self, document_page_id=None,
                                access_token=None, **kw):
        try:
            document_page_sudo = self._document_check_access(
                'document.page', document_page_id, access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')

        values = self._document_page_get_page_view_values(
            document_page_sudo, access_token, **kw)
        return request.render(
            "document_page_portal.document_pages_followup", values)
