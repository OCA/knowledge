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
    "name": "Choose a document's directory during upload",
    "version": "1.0",
    "author": "Therp BV,Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "complexity": "normal",
    "description": """
Introduction
============

This addons enables users to choose a directory while uploading a file. In
combination with access permissions on directories, this can be used to
restrict access on certain records' attachments or simply for a better
overview.

Configuration
=============

Create a static directory and choose the resource model you want to use this
directory on. Assign groups to whom this directory should be accessible. When
uploading a files, users can select one of the directories they have access to,
or no directory which is the default setting.

Keep in mind that if a directory has a owner, it's only visible for this user,
that's probably not what you want.
    """,
    "category": "Knowledge",
    "depends": [
        'document',
        'web',
    ],
    "data": [
        "view/document_directory.xml",
    ],
    "js": [
        'static/src/js/document_choose_directory.js',
    ],
    "css": [
        'static/src/css/document_choose_directory.css',
    ],
    "qweb": [
        'static/src/xml/document_choose_directory.xml',
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
