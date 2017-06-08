openerp.cmis_read = function(instance, m) {
var _t = instance.web._t,
    QWeb = instance.web.qweb;

    instance.web.Sidebar.include({
        redraw: function() {
            var self = this;
            this._super.apply(this, arguments);
            self.$el.find('.oe_sidebar_add_attachment').after(QWeb.render('AddDocfromdms', {widget: self}))
            self.$el.find('.oe_sidebar_add_dms_doc').on('click', function (e) {
                self.on_cmis_doc();
            });
        },
        on_cmis_doc: function(state) {
            var self = this;
            var view = self.getParent();
            var ids = ( view.fields_view.type != "form" )? view.groups.get_selection().ids : [ view.datarecord.id ];
            var ds = new instance.web.DataSet(this, 'ir.attachment', context);
            // you can pass in other data using the context dictionary variable
            var context = {
            'model': view.dataset.model,
            'ids': ids,
            };
            // the action dictionary variable sends data in the "self.do_action" method
            var action = {
                name: _t("Search Document from DMS"),
                type: 'ir.actions.act_window',
                res_model: 'ir.attachment.dms.wizard',
                view_mode: 'form',
                view_type: 'form',
                views: [[false, 'form']],
                target: 'new',
                context: context,
            };
            // self.do_action accepts the action parameter and opens the new view
            self.do_action(action, {
                // refresh list of documents
                on_close: function () {
                    self.do_attachement_update(self.dataset, self.model_id);
                }
            });
        }
    });
};
