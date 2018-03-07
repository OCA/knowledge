//-*- coding: utf-8 -*-
//© 2017 Therp BV <http://therp.nl>
//License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

openerp.document_wopi = function(instance)
{
    var _t = instance.web._t;
    instance.web.Sidebar.include(
    {
        on_attachments_loaded: function(attachments)
        {
            var self = this;
            return jQuery.when(this._super.apply(this, arguments))
            .then(function()
            {
                self.$el.find('.oe-sidebar-document-wopi')
                .click(self.on_document_wopi);
            });
        },
        on_document_wopi: function(e)
        {
            var self = this,
                $target = jQuery(e.currentTarget),
                attachment_id = $target.data('id');
            e.preventDefault();
            e.stopPropagation();
            return new instance.web.Model('document.wopi').call(
                'get_access_token', [attachment_id]
            ).then(function(access_token_id)
            {
                return self.document_wopi_frame(access_token_id);
            });
        },
        document_wopi_frame: function(access_token_id)
        {
            this.do_action({
                type: 'ir.actions.client',
                name: 'document_wopi',
                tag: 'document_wopi',
                params: {
                    access_token_id: access_token_id,
                }
            });
        },
    });
    instance.document_wopi.OfficeWidget = instance.web.Widget.extend({
        'template': 'DocumentWopiOfficeWidget',
        init: function(parent, options)
        {
            this.params = options.params;
            return this._super.apply(this, arguments);
        },
        start: function()
        {
            return this._super.apply(this, arguments)
            .then(this.proxy('get_token_values'))
            .then(this.proxy('call_wopi_client'));
        },
        get_token_values: function()
        {
            var self = this;
            return new instance.web.Model('document.wopi.access.token').query(
                ['token', 'token_ttl', 'attachment_id', 'action_url']
            )
            .filter([['id', '=', this.params.access_token_id]])
            .first()
            .then(function(data)
            {
                self.params = _.extend(self.params, data);
            });
        },
        call_wopi_client: function()
        {
            if(!this.params.action_url)
            {
                throw instance.web._t('Unsupported document!');
            }
            this.$('form').attr('action', this.params.action_url);
            this.$('form input[name="access_token"]').val(this.params.token);
            this.$('form input[name="access_token_ttl"]').val(
                this.params.token_ttl
            );
            this.$('form').submit();
        },
    });
    instance.web.client_actions.add(
        'document_wopi', 'instance.document_wopi.OfficeWidget'
    );
};
