/** @odoo-module **/
/* Copyright 2026 Jarsa
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl). */

import {FileViewer} from "@web/core/file_viewer/file_viewer";
import {XmlViewer} from "./xml_viewer.esm";
import {patch} from "@web/core/utils/patch";

patch(FileViewer, {
    components: {...FileViewer.components, XmlViewer},
});
