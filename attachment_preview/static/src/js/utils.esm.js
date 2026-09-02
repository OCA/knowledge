import {Component} from "@odoo/owl";

// PDFs are rendered directly by Odoo's native PDF.js viewer.
const PDF_EXTENSIONS = ["pdf"];

// Office formats (ODF + OOXML + legacy) are converted to PDF server-side via
// the /attachment_preview/office_to_pdf endpoint, then rendered through the
// same native PDF.js viewer. ViewerJS is no longer used.
const OFFICE_EXTENSIONS = [
    "odt",
    "ods",
    "odp",
    "odg",
    "fodt",
    "fods",
    "fodp",
    "ott",
    "ots",
    "otp",
    "doc",
    "docx",
    "xls",
    "xlsx",
    "ppt",
    "pptx",
];

export function canPreview(extension) {
    return PDF_EXTENSIONS.includes(extension) || OFFICE_EXTENSIONS.includes(extension);
}

export function isOfficeExtension(extension) {
    return OFFICE_EXTENSIONS.includes(extension);
}

// Build a URL to Odoo core's bundled PDF.js viewer — the very viewer its native
// FileViewer uses for PDF attachments (see web .../core/file_viewer/file_model.js).
function pdfViewerUrl(pdfRoute) {
    const origin = window.location.origin || "";
    return (
        origin +
        "/web/static/lib/pdfjs/web/viewer.html?file=" +
        encodeURIComponent(pdfRoute) +
        "#pagemode=none"
    );
}

// Build the LibreOffice->PDF conversion route for an office attachment.
function officeConversionRoute(
    attachment_id,
    attachment_url,
    attachment_extension,
    attachment_filename
) {
    const origin = window.location.origin || "";
    const filename = attachment_filename || "file." + attachment_extension;

    if (attachment_url) {
        // Derive model/field/id from the binary field URL,
        // e.g. /web/content?model=dms.file&field=content&id=42
        try {
            const parsed = new URL(origin + attachment_url);
            const model = parsed.searchParams.get("model");
            const field = parsed.searchParams.get("field");
            const id = parsed.searchParams.get("id");
            if (model && field && id) {
                return (
                    "/attachment_preview/office_to_pdf?model=" +
                    encodeURIComponent(model) +
                    "&field=" +
                    encodeURIComponent(field) +
                    "&id=" +
                    encodeURIComponent(id) +
                    "&filename=" +
                    encodeURIComponent(filename)
                );
            }
        } catch {
            // Fall through to the attachment_id path.
        }
    }
    if (attachment_id) {
        return (
            "/attachment_preview/office_to_pdf?model=ir.attachment" +
            "&field=datas&id=" +
            attachment_id +
            "&filename=" +
            encodeURIComponent(filename)
        );
    }
    return "";
}

export function getUrl(
    attachment_id,
    attachment_url,
    attachment_extension,
    attachment_title,
    attachment_filename
) {
    const origin = window.location.origin || "";

    // Office formats (ODF + OOXML): convert to PDF, then render via PDF.js.
    if (isOfficeExtension(attachment_extension)) {
        const route = officeConversionRoute(
            attachment_id,
            attachment_url,
            attachment_extension,
            attachment_filename
        );
        if (route) {
            return pdfViewerUrl(route);
        }
    }

    // PDFs render directly through the native viewer.
    let pdfRoute = "";
    if (attachment_url) {
        // Already a fully-built pdf.js viewer URL -> use as-is.
        if (attachment_url.indexOf("/web/static/lib/pdfjs") !== -1) {
            return attachment_url.startsWith("http")
                ? attachment_url
                : origin + attachment_url;
        }
        pdfRoute = attachment_url.replace(origin, "");
    } else if (attachment_id) {
        pdfRoute = "/web/content/" + attachment_id + "?model=ir.attachment";
    }
    return pdfViewerUrl(pdfRoute);
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
