import {canPreview, showPreview} from "../../utils.esm";
import {useLayoutEffect} from "@web/owl2/utils";
import {BinaryField} from "@web/views/fields/binary/binary_field";
import {_t} from "@web/core/l10n/translation";
import {patch} from "@web/core/utils/patch";
import {sprintf} from "@web/core/utils/strings";
import {proxy} from "@odoo/owl";
import {useService} from "@web/core/utils/hooks";

patch(BinaryField.prototype, {
    setup() {
        super.setup();
        this.orm = useService("orm");
        this.previewState = proxy({extension: ""});
        // Recheck saved files after uploads and navigation, without previewing stale data.
        useLayoutEffect(
            () => {
                let active = true;
                this.previewState.extension = "";
                const {record, name, fileNameField} = this.props;
                if (record.resId && !record.dirty && record.data[name]) {
                    this.orm
                        .call("ir.attachment", "get_binary_extension", [
                            record.resModel,
                            record.resId,
                            name,
                            fileNameField,
                        ])
                        .then((extension) => {
                            if (active) {
                                this.previewState.extension = extension;
                            }
                        });
                }
                return () => {
                    active = false;
                };
            },
            () => [
                this.props.record.resModel,
                this.props.record.resId,
                this.props.record.dirty,
                this.props.name,
                this.props.fileNameField,
                this.props.record.data[this.props.name],
                this.props.record.data[this.props.fileNameField],
            ]
        );
    },

    get canPreviewBinary() {
        const {record, name} = this.props;
        return (
            record.resId &&
            !record.dirty &&
            record.data[name] &&
            canPreview(this.previewState.extension)
        );
    },

    _onPreview() {
        if (!this.canPreviewBinary) {
            return;
        }
        const params = new URLSearchParams({
            model: this.props.record.resModel,
            field: this.props.name,
            id: this.props.record.resId,
        });
        showPreview(
            null,
            `/web/content?${params}`,
            this.previewState.extension,
            sprintf(_t("Preview %s"), this.fileName),
            false,
            null
        );
    },
});
