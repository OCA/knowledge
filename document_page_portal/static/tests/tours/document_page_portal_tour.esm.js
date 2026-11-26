/** @odoo-module **/
/* Copyright 2020 - TODAY, Marcel Savegnago - Escodoo
   License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl). */

import {registry} from "@web/core/registry";

registry.category("web_tour.tours").add("document_page_portal_tour", {
    url: "/my",
    steps: () => [
        {
            content: "Check document_page_portal is loaded",
            trigger:
                'a[href*="/my/knowledge/documents"]:contains("Knowledge Documents"):first',
            run: "click",
        },
        {
            content: "Check public document_page is loaded",
            trigger:
                'a[href*="/knowledge/document/"]:contains("Test Public Page 1"):first',
            run: "click",
        },
        {
            content: "Verify the document page rendered",
            trigger: 'h1:contains("Test Public Page 1")',
        },
    ],
});

registry.category("web_tour.tours").add("document_page_portal_search_tour", {
    url: "/my/knowledge/documents",
    steps: () => [
        {
            content: "Search",
            trigger: "input[name='search']",
            run: "edit Test",
        },
        {
            content: "Click Search.",
            trigger: ".o_portal_navbar button[type='submit']",
            run: "click",
        },
        {
            content: "Verify the matching document is in the search results",
            trigger: 'a[href*="/knowledge/document/"]:contains("Test Public Page 1")',
        },
    ],
});
