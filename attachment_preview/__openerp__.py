# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2014 Therp BV (<http://therp.nl>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    "name": "Preview attachments",
    "version": "1.0",
    "author": "Therp BV,Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "complexity": "normal",
    "description": """
This addon allows to preview attachments supported by http://viewerjs.org.

Currently, that's most Libreoffice files and PDFs.

For filetype recognition, you'll get the best results by installing
``python-magic``.

Acknowledgements
================

Addon icon courtesy of http://commons.wikimedia.org/wiki/Crystal_Clear
    """,
    "category": "Knowledge Management",
    "depends": [
        'web'
    ],
    "data": [
    ],
    "js": [
        'static/src/js/attachment_preview.js',
    ],
    "css": [
        'static/src/css/attachment_preview.css',
    ],
    "qweb": [
        'static/src/xml/attachment_preview.xml',
    ],
    "test": [
    ],
    "auto_install": False,
    "installable": True,
    "application": False,
    "external_dependencies": {
        'python': [],
    },
}
