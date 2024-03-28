/** @odoo-module **/
import {canPreview, getUrl} from "../utils.esm";
import {query} from "web.rpc";
import {registerPatch} from "@mail/model/model_core";

registerPatch({
    name: "AttachmentList",
    lifecycleHooks: {
        _created() {
            var attachments = _.object(
                this.attachments.map((attachment) => {
                    return attachment.id;
                }),
                this.attachments.map((attachment) => {
                    if (
                        attachment.defaultSource &&
                        attachment.defaultSource.length > 38
                    ) {
                        return {
                            url: attachment.defaultSource,
                            extension: attachment.extension,
                            title: attachment.name,
                        };
                    }
                    return {
                        url: "/web/content?id=" + attachment.id + "&download=true",
                        extension: attachment.extension,
                        title: attachment.name,
                    };
                })
            );

            var self = this;
            query({
                model: "ir.attachment",
                method: "get_attachment_extension",
                args: [
                    _.map(_.keys(attachments), function (id) {
                        return parseInt(id, 10);
                    }),
                ],
            }).then(function (extensions) {
                self.previewableAttachments = _.map(
                    _.keys(
                        _.pick(extensions, function (extension) {
                            return canPreview(extension);
                        })
                    ),
                    function (id) {
                        return {
                            id: id,
                            url: attachments[id].url,
                            extension: extensions[id],
                            title: attachments[id].title,
                            previewUrl: getUrl(
                                id,
                                attachments[id].url,
                                extensions[id],
                                attachments[id].title
                            ),
                        };
                    }
                );
            });
        },
    },
});
