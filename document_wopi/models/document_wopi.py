# -*- coding: utf-8 -*-
# © 2017 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import requests
import urlparse
from openerp import api, models, tools
from lxml import etree


class DocumentWopi(models.AbstractModel):
    _name = 'document.wopi'
    _description = 'Implement the WOPI protocol'

    @api.model
    def _get_url(self, path):
        client = self.env['ir.config_parameter'].get_param(
            'document_wopi.client'
        )
        assert client, 'You need to define your WOPI client in the settings'
        return urlparse.urljoin(client, path)

    @api.model
    def _call(self, path, query=None, headers=None):
        return requests.get(
            self._get_url(path), params=query, headers=headers
        )

    @api.model
    def get_access_token(self, attachment_id):
        """Return an access token to pass to the WOPI client. Make sure the
        user in question can access the resource"""
        self.env['ir.attachment'].browse(attachment_id).read([])
        return self.env['document.wopi.access.token']._get_token(
            self.env['ir.attachment'].browse(attachment_id)
        ).id

    @tools.ormcache()
    @api.model
    def _discovery(self):
        response = self.env['document.wopi']._call('hosting/discovery')
        xml = etree.fromstring(response.text)
        result = {}
        for action in xml.xpath('//action'):
            ext = action.attrib['ext']
            name = action.attrib['name']
            result[(ext, name)] = dict(action.attrib)
        return result
