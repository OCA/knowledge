/** @odoo-module **/

import {loadJS} from "@web/core/assets";
import {registerMessagingComponent} from "@mail/utils/messaging_component";
import {useComponentToModel} from "@mail/component_hooks/use_component_to_model";
import {useService} from "@web/core/utils/hooks";

const {Component, onWillStart, useState} = owl;

export class AttachmentGooglePicker extends Component {
    /**
     * @override
     */
    setup() {
        super.setup();
        useComponentToModel({fieldName: "component"});
        this.orm = useService("orm");
        this.user = useService("user");
        this.action = useService("action");
        this.state = useState({
            pickerInited: false,
            gisInited: false,
            api_key: "",
            scopes: "",
            client_id: "",
            app_id: "",
            accessToken: null,
            expiresDate: 0,
        });
        this.tokenClient = null;

        onWillStart(async () => {
            await this.getUserAuthParams();
            if (!this.checkActive()) {
                return;
            }
            await loadJS("https://apis.google.com/js/api.js", {
                attrs: {async: true, defer: true},
            });
            await this.gapiLoaded();
            await loadJS("https://accounts.google.com/gsi/client", {
                attrs: {async: true, defer: true},
            });
            await this.gisLoaded();
        });
    }

    // --------------------------------------------------------------------------
    // Public
    // --------------------------------------------------------------------------

    async _onAddGooglePickerUrl() {
        if (
            this.state.accessToken &&
            this.state.expiresDate > Math.floor(Date.now() / 1000)
        ) {
            await this.createPicker();
        } else {
            await this.handleAuthClick();
        }
    }

    checkActive() {
        return (
            Boolean(this.state.api_key) &&
            Boolean(this.state.scopes) &&
            Boolean(this.state.client_id) &&
            Boolean(this.state.app_id)
        );
    }

    async _onSignOut() {
        this.state.accessToken = null;
        await this.saveUserAuthAccessToken();
    }
    // --------------------------------------------------------------------------
    // Private
    // --------------------------------------------------------------------------

    async getUserAuthParams() {
        const res = await this.orm.call("res.users", "get_google_picker_params", [
            this.user.userId,
        ]);
        if (!res) {
            return;
        }
        this.state.client_id = res.client_id;
        this.state.api_key = res.api_key;
        this.state.app_id = res.app_id;
        this.state.scopes = res.scope;
        this.state.accessToken = res.access_token;
        this.state.expiresDate = res.expires_date;
        this.state.mime_types = res.mime_types;
    }

    async saveUserAuthAccessToken() {
        await this.orm.call("res.users", "save_google_picker_access_token", [
            this.user.userId,
            this.state.accessToken,
            this.state.expiresDate,
        ]);
    }

    async gapiLoaded() {
        window.gapi.load("client:picker", this.initializePicker.bind(this));
    }

    async initializePicker() {
        await window.gapi.client.load(
            "https://www.googleapis.com/discovery/v1/apis/drive/v3/rest"
        );
        this.state.pickerInited = true;
    }

    handleAuthClick() {
        this.tokenClient.callback = async (response) => {
            if (response.error !== undefined) {
                throw response;
            }
            this.state.accessToken = response.access_token;
            this.state.expiresDate =
                Math.floor(Date.now() / 1000) + response.expires_in;
            await this.createPicker();
            await this.saveUserAuthAccessToken();
        };

        if (this.state.accessToken === null) {
            // Prompt the user to select a Google Account and ask for consent to share their data
            // when establishing a new session.
            this.tokenClient.requestAccessToken({
                prompt: "consent",
                access_type: "offline",
            });
        } else {
            // Skip display of account chooser and consent dialog for an existing session.
            this.tokenClient.requestAccessToken({prompt: "", access_type: "offline"});
        }
    }

    async gisLoaded() {
        this.tokenClient = window.google.accounts.oauth2.initTokenClient({
            client_id: this.state.client_id,
            scope: this.state.scopes,
            callback: "",
        });
        this.state.gisInited = true;
    }

    createPicker() {
        const view = new window.google.picker.View(window.google.picker.ViewId.DOCS);
        if (this.state.mime_types) {
            view.setMimeTypes(this.state.mime_types);
        }
        const picker = new window.google.picker.PickerBuilder()
            .enableFeature(window.google.picker.Feature.NAV_HIDDEN)
            .enableFeature(window.google.picker.Feature.MULTISELECT_ENABLED)
            .setDeveloperKey(this.state.api_key)
            .setAppId(this.state.app_id)
            .setOAuthToken(this.state.accessToken)
            .addView(view)
            .addView(new window.google.picker.DocsUploadView())
            .setCallback(this.pickerCallback.bind(this))
            .build();
        picker.setVisible(true);
    }

    async pickerCallback(data) {
        if (data.action === window.google.picker.Action.PICKED) {
            for (const document of data.docs) {
                await this.createAttachment(document);
            }
            await this._onAddedUrl();
        }
    }

    async createAttachment(document) {
        await this.orm.call("ir.attachment.add_url", "add_attachment_google_drive", [
            document.url,
            document.name,
            this.props.record.chatter.thread.model,
            [this.props.record.chatter.thread.id],
        ]);
    }

    async _onAddedUrl() {
        this.props.record.chatter.refresh();
    }
}

Object.assign(AttachmentGooglePicker, {
    props: {record: Object},
    template: "document_url_google_drive.GooglePickerUrl",
});

registerMessagingComponent(AttachmentGooglePicker);
