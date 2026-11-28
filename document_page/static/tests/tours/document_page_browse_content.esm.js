/* Copyright 2026 NuoBiT Solutions SL - Eric Antones <eantones@nuobit.com>
   License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl). */

import {registry} from "@web/core/registry";

registry.category("web_tour.tours").add("document_page_browse_content", {
    steps: () => [
        {
            content: "Open the folder from its card",
            trigger: '.o_kanban_record:contains("Outer Folder")',
            run: "click",
        },
        {
            content: "Check that the breadcrumb shows the folder",
            trigger: '.o_last_breadcrumb_item:contains("Outer Folder")',
        },
        {
            content: "Check that the folder shows its content",
            trigger: '.o_kanban_record:contains("Inner Folder")',
        },
        {
            content: "Check that the folder shows no other content",
            trigger:
                '.o_kanban_view:not(:has(.o_kanban_record:contains("Other Folder")))',
        },
        {
            content: "Open its subfolder from its card",
            trigger: '.o_kanban_record:contains("Inner Folder")',
            run: "click",
        },
        {
            content: "Check that the breadcrumb shows the subfolder",
            trigger: '.o_last_breadcrumb_item:contains("Inner Folder")',
        },
        {
            content: "Go back to the folder",
            trigger: '.breadcrumb-item:contains("Outer Folder")',
            run: "click",
        },
        {
            content: "Check that the breadcrumb shows the folder again",
            trigger: '.o_last_breadcrumb_item:contains("Outer Folder")',
        },
        {
            content: "Check that the folder shows its content again",
            trigger: '.o_kanban_record:contains("Inner Folder")',
        },
    ],
});
