import {Component} from "@odoo/owl";

// Extensions rendered natively by ViewerJS (PDF + ODF formats)
const VIEWERJS_EXTENSIONS = [
    "odt",
    "odp",
    "ods",
    "fodt",
    "pdf",
    "ott",
    "fodp",
    "otp",
    "fods",
    "ots",
];

// Extensions converted to PDF server-side via LibreOffice (if installed).
// These use the /attachment_preview/office_to_pdf endpoint.
const OFFICE_EXTENSIONS = ["docx", "xlsx", "pptx", "doc", "xls", "ppt", "odg"];

export function canPreview(extension) {
    return (
        VIEWERJS_EXTENSIONS.includes(extension) || OFFICE_EXTENSIONS.includes(extension)
    );
}

export function isOfficeExtension(extension) {
    return OFFICE_EXTENSIONS.includes(extension);
}

export function getUrl(
    attachment_id,
    attachment_url,
    attachment_extension,
    attachment_title,
    attachment_filename
) {
    var origin = window.location.origin || "";

    // Office formats: route through LibreOffice → PDF conversion endpoint
    if (isOfficeExtension(attachment_extension)) {
        var conversionUrl = "";
        if (attachment_url) {
            // Derive model/field/id from the binary field URL
            // e.g. /web/content?model=dms.file&field=content&id=42
            try {
                var parsed = new URL(origin + attachment_url);
                var model = parsed.searchParams.get("model");
                var field = parsed.searchParams.get("field");
                var id = parsed.searchParams.get("id");
                if (model && field && id) {
                    conversionUrl =
                        origin +
                        "/attachment_preview/office_to_pdf" +
                        "?model=" +
                        encodeURIComponent(model) +
                        "&field=" +
                        encodeURIComponent(field) +
                        "&id=" +
                        encodeURIComponent(id) +
                        "&filename=" +
                        encodeURIComponent(
                            attachment_filename || "file." + attachment_extension
                        );
                }
            } catch {
                // URL parsing failed — fall through to attachment_id path
            }
        }
        if (!conversionUrl && attachment_id) {
            conversionUrl =
                origin +
                "/attachment_preview/office_to_pdf" +
                "?model=ir.attachment&field=datas&id=" +
                attachment_id +
                "&filename=" +
                encodeURIComponent(
                    attachment_filename || "file." + attachment_extension
                );
        }
        if (conversionUrl) {
            // Tell ViewerJS the converted output is PDF
            return (
                origin +
                "/attachment_preview/static/lib/ViewerJS/index.html" +
                "?type=pdf" +
                "&title=" +
                encodeURIComponent(attachment_title) +
                "&zoom=automatic" +
                "#" +
                conversionUrl.replace(origin, "")
            );
        }
    }

    // Native ViewerJS path (PDF + ODF)
    var url = "";
    if (attachment_url) {
        if (attachment_url.slice(0, 21) === "/web/static/lib/pdfjs") {
            url = origin + attachment_url;
        } else {
            url =
                origin +
                "/attachment_preview/static/lib/ViewerJS/index.html" +
                "?type=" +
                encodeURIComponent(attachment_extension) +
                "&title=" +
                encodeURIComponent(attachment_title) +
                "&zoom=automatic" +
                "#" +
                attachment_url.replace(origin, "");
        }
        return url;
    }
    url =
        origin +
        "/attachment_preview/static/lib/ViewerJS/index.html" +
        "?type=" +
        encodeURIComponent(attachment_extension) +
        "&title=" +
        encodeURIComponent(attachment_title) +
        "&zoom=automatic" +
        "#" +
        "/web/content/" +
        attachment_id +
        "?model%3Dir.attachment";

    return url;
}

export function showPreview(
    attachment_id,
    attachment_url,
    attachment_extension,
    attachment_title,
    split_screen,
    attachment_info_list,
    attachment_filename
) {
    if (split_screen && attachment_info_list) {
        Component.env.bus.trigger("open_attachment_preview", {
            attachment_id,
            attachment_info_list,
        });
    } else {
        window.open(
            getUrl(
                attachment_id,
                attachment_url,
                attachment_extension,
                attachment_title,
                attachment_filename
            )
        );
    }
}
