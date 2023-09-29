/** @odoo-module **/
import {bus} from "web.core";

export function canPreview(extension) {
    return (
        $.inArray(extension, [
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
        ]) > -1
    );
}

export function getUrl(
    attachment_id,
    attachment_url,
    attachment_extension,
    attachment_title
) {
    var url = "";
    if (attachment_url) {
        if (attachment_url.slice(0, 21) === "/web/static/lib/pdfjs") {
            url = (window.location.origin || "") + attachment_url;
        } else {
            url =
                (window.location.origin || "") +
                "/attachment_preview/static/lib/ViewerJS/index.html" +
                "?type=" +
                encodeURIComponent(attachment_extension) +
                "&title=" +
                encodeURIComponent(attachment_title) +
                "&zoom=automatic" +
                "#" +
                attachment_url.replace(window.location.origin, "");
        }
        return url;
    }
    url =
        (window.location.origin || "") +
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
    attachment_info_list
) {
    if (split_screen && attachment_info_list) {
        bus.trigger("open_attachment_preview", attachment_id, attachment_info_list);
    } else {
        window.open(
            getUrl(
                attachment_id,
                attachment_url,
                attachment_extension,
                attachment_title
            )
        );
    }
}
