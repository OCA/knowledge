odoo.define("document_page_portal.tour", function(require) {
    "use strict";

    var tour = require("web_tour.tour");

    tour.register(
        "document_page_portal_tour",
        {
            test: true,
            url: "/my",
        },
        [
            {
                content: "Check document_page_portal is loaded",
                trigger:
                    'a[href*="/my/knowledge/documents"]:contains("Knowledge Documents"):first',
            },
            {
                content: "Check public document_page is loaded",
                trigger:
                    'a[href*="/knowledge/document/"]:contains("Test Public Page 1"):first',
            },
        ]
    );

    tour.register(
        "document_page_portal_search_tour",
        {
            test: true,
            url: "/my/knowledge/documents",
        },
        [
            {
                content: "Search",
                trigger: "input[name='search']",
                run: "text Test",
            },
            {
                content: "Click Search.",
                extra_trigger: "#wrap:not(:has(input[name=search]:propValue('')))",
                trigger: ".search-submit",
            },
        ]
    );
});
