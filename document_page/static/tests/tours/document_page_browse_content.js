/* Copyright 2026 NuoBiT Solutions SL - Eric Antones <eantones@nuobit.com>
   License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl). */

odoo.define("document_page.browse_content_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    tour.register("document_page_browse_content", {test: true}, [
        {
            content: "Open the folder from its card",
            trigger: '.o_kanban_record:contains("Outer Folder")',
        },
        {
            content: "Check that the folder shows its content",
            extra_trigger: '.breadcrumb-item.active:contains("Outer Folder")',
            trigger: '.o_kanban_record:contains("Inner Folder")',
            run: function () {
                // Only a check
            },
        },
        {
            content: "Check that the folder shows no other content",
            trigger:
                '.o_kanban_view:not(:has(.o_kanban_record:contains("Other Folder")))',
            run: function () {
                // Only a check
            },
        },
        {
            content: "Open its subfolder from its card",
            trigger: '.o_kanban_record:contains("Inner Folder")',
        },
        {
            content: "Go back to the folder",
            extra_trigger: '.breadcrumb-item.active:contains("Inner Folder")',
            trigger: '.breadcrumb-item:contains("Outer Folder")',
        },
        {
            content: "Check that the folder shows its content again",
            extra_trigger: '.breadcrumb-item.active:contains("Outer Folder")',
            trigger: '.o_kanban_record:contains("Inner Folder")',
            run: function () {
                // Only a check
            },
        },
    ]);
});
