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
                name: _t("Add existing document"),
                type: 'ir.actions.act_window',
                res_model: 'ir.attachment.existing.doc',
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

        },
        on_attachment_delete: function(e) {
            e.preventDefault();
            e.stopPropagation();
            var self = this;
            var view = self.getParent();
            self.model_view = view.dataset.model
            var ids = ( view.fields_view.type != "form" )? view.groups.get_selection().ids : [ view.datarecord.id ];
            // Context dictionary variable
            var context = {
                'multiple_records_res_model':  self.model_view,
                'multiple_records_res_id': ids[0],
            };
            var $e = $(e.currentTarget);
            if (confirm(_t("Do you really want to delete this attachment ?"))) {
                (new instance.web.DataSet(this, 'ir.attachment', context)).unlink([parseInt($e.attr('data-id'), 10)]).done(function() {
                self.do_attachement_update(self.dataset, self.model_id);
                });
            }
        },
        do_attachement_update: function(dataset, model_id, args) {
            var self = this;
            this.dataset = dataset;
            this.model_id = model_id;
            // Add the model and the model_id in the context
            var context = {
                'model': dataset.model,
                'model_id': model_id
            };
            if (args && args[0].error) {
                this.do_warn(_t('Uploading Error'), args[0].error);
            }
            if (!model_id) {
                this.on_attachments_loaded([]);
            }
            else {
                var dom = [ ['related_document', '=', true] ];
                var ds = new instance.web.DataSetSearch(this, 'ir.attachment', context, dom);
                ds.read_slice(['name', 'url', 'type', 'create_uid', 'create_date', 'write_uid', 'write_date'], {}).done(this.on_attachments_loaded);
            }
        }
    });
};
