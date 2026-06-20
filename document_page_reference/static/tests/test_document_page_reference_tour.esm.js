/** @odoo-module */

import tour from "web_tour.tour";

/*
 * Test 1: Reference widget renders ${ref} as clickable links.
 */
tour.register(
    "document_page_reference_widget_tour",
    {
        test: true,
        url: "/web#action=document_page.action_page",
    },
    [
        {
            content: "Open Test Ref Page 1",
            trigger: '.o_data_cell[name="name"]:contains("Test Ref Page 1")',
            run: "click",
        },
        {
            content: "Verify content_parsed renders reference as link",
            trigger:
                '.o_form_view .o_field_widget[name="content_parsed"] a.oe_direct_line',
            timeout: 20000,
            run: function () {
                var link = this.$anchor[0];
                if (!link.dataset.oeModel || !link.dataset.oeId) {
                    throw new Error("Reference link missing data-oe-model/data-oe-id");
                }
                if (link.getAttribute("target") === "_blank") {
                    throw new Error(
                        "Internal reference link should not have target=_blank"
                    );
                }
            },
        },
    ]
);

/*
 * Test 2: Category page index uses oe_direct_line links.
 */
tour.register(
    "document_page_reference_category_tour",
    {
        test: true,
        url: "/web#action=document_page.action_page",
    },
    [
        {
            content: "Open Test Ref Page 1 to navigate to its category",
            trigger: '.o_data_cell[name="name"]:contains("Test Ref Page 1")',
            run: "click",
        },
        {
            content: "Navigate to category via parent_id link",
            trigger: '.o_form_view .o_field_widget[name="parent_id"] a',
            timeout: 20000,
            run: "click",
        },
        {
            content: "Verify category shows child links as oe_direct_line",
            trigger:
                '.o_form_view .o_field_widget[name="content_parsed"] a.oe_direct_line',
            timeout: 20000,
            run: function () {
                var links = document.querySelectorAll(
                    '.o_field_widget[name="content_parsed"] a.oe_direct_line'
                );
                if (links.length < 1) {
                    throw new Error("Category should have child page links");
                }
                // Verify links have correct attributes
                var link = links[0];
                if (!link.dataset.oeModel || !link.dataset.oeId) {
                    throw new Error("Category index link missing data-oe-model/id");
                }
                if (link.getAttribute("target") === "_blank") {
                    throw new Error("Category index link should not open in new tab");
                }
            },
        },
    ]
);
