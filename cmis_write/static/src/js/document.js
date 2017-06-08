openerp.cmis_write = function(instance, m) {
var _t = instance.web._t,
    QWeb = instance.web.qweb;

    instance.web.Sidebar.include({
        start: function() {
        var self = this;
        this._super(this);
        this.redraw();
        this.$el.on('click','.oe_dropdown_menu li a', function(event) {
            var section = $(this).data('section');
            var index = $(this).data('index');
            var item = self.items[section][index];
            if (item.callback) {
                item.callback.apply(self, [item]);
            } else if (item.action) {
                self.on_item_action_clicked(item);
            } else if (!item.id_dms) {
                alert(_t("Document is not available in DMS.Please try again !!!"));
            } else if (item.url) {
                return true;
            }
            event.preventDefault();
        });
    },
    do_attachement_update: function(dataset, model_id, args) {
        var self = this;
        this.dataset = dataset;
        this.model_id = model_id;
        if (args && args[0].error) {
            this.do_warn(_t('Uploading Error'), args[0].error);
        }
        if (!model_id) {
            this.on_attachments_loaded([]);
        } else {
            var dom = [ ['res_model', '=', dataset.model], ['res_id', '=', model_id], ['type', 'in', ['binary', 'url']] ];
            var ds = new instance.web.DataSetSearch(this, 'ir.attachment', dataset.get_context(), dom);
            ds.read_slice(['name', 'url', 'id_dms','type', 'create_uid', 'create_date', 'write_uid', 'write_date'], {}).done(this.on_attachments_loaded);
        }
    },
    });
};
