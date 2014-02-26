openerp.document_multiple_records = function(instance, m) {
var _t = instance.web._t,
    QWeb = instance.web.qweb;

    instance.web.Sidebar.include({
        redraw: function() {
            var self = this;
            this._super.apply(this, arguments);
            self.$el.find('.oe_sidebar_add_attachment').after(QWeb.render('AddDocfromserver', {widget: self}))
            self.$el.find('.open').on('click', function (e) {
                self.on_call_new_view_function();
            });
        },
        on_call_new_view_function: function(state) {
            var self = this;
            var view = self.getParent();
            var ids = ( view.fields_view.type != "form" )? view.groups.get_selection().ids : [ view.datarecord.id ];
            // you can pass in other data using the context dictionary variable
            var context = {
            'model': view.dataset.model,
            'ids': ids,
            };
            // the action dictionary variable sends data in the "self.do_action" method
            var action = {
                name: _t("Add existing document/attachment"),
                type: 'ir.actions.act_window',
                res_model: 'ir.attachment.existing.doc',
                view_mode: 'form',
                view_type: 'form',
                views: [[false, 'form']],
                target: 'new',
                context: context,
            };
            // self.do_action accepts the action parameter and opens the new view
            self.do_action(action);
        }
    });
};
