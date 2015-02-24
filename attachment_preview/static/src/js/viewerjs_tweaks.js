//-*- coding: utf-8 -*-
//############################################################################
//
//   OpenERP, Open Source Management Solution
//   This module copyright (C) 2014 Therp BV (<http://therp.nl>).
//
//   This program is free software: you can redistribute it and/or modify
//   it under the terms of the GNU Affero General Public License as
//   published by the Free Software Foundation, either version 3 of the
//   License, or (at your option) any later version.
//
//   This program is distributed in the hope that it will be useful,
//   but WITHOUT ANY WARRANTY; without even the implied warranty of
//   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//   GNU Affero General Public License for more details.
//
//   You should have received a copy of the GNU Affero General Public License
//   along with this program.  If not, see <http://www.gnu.org/licenses/>.
//
//############################################################################

// This file contains tweaks for viewerjs itself and is not meant to be run in
// OpenERP's context
var original_loadDocument = loadDocument;
loadDocument = function(documentUrl)
{
    original_loadDocument.apply(this, arguments);
    var original_onload = window.onload;
    window.onload = function()
    {
        original_onload();
        var matches = (/&title=([^&]+)&/).exec(window.location.hash);
        if(matches && matches.length > 1)
        {
            document.title = decodeURIComponent(matches[1]);
            document.getElementById('documentName').innerHTML = document.title;

        }
    };
}
