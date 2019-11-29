odoo.define('document_page_reference.backend', function (require) {
    'use strict';

    var field_registry = require('web.field_registry');
    var backend = require('web_editor.backend');
    var FieldTextHtmlSimple = backend.FieldTextHtmlSimple;

    var FieldDocumentPage = FieldTextHtmlSimple.extend({
        events: _.extend({}, FieldTextHtmlSimple.prototype.events, {
            'click .oe_direct_line': '_onClickDirectLink',
        }),
        _onClickDirectLink: function (event) {
            var self = this;
            event.preventDefault();
            event.stopPropagation();
            var element = $(event.target).closest('.oe_direct_line')[0];
            var default_reference = element.name;
            var model = $(event.target).data('oe-model');
            var id = $(event.target).data('oe-id');
            var context = this.record.getContext(this.recordParams);
            if (default_reference){
                context['default_reference'] = default_reference
            }
            this._rpc({
                model: model,
                method: 'get_formview_action',
                args: [[parseInt(id)]],
                context: context,
            })
            .then(function (action) {
                self.trigger_up('do_action', {action: action});
            });
        },
    });
    field_registry.add('document_page_reference', FieldDocumentPage);
    return FieldDocumentPage;
});
