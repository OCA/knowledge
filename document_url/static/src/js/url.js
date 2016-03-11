/* © 2014 Serv. Tecnol. Avanzados (http://www.serviciosbaeza.com)
 *                      Pedro M. Baeza <pedro.baeza@serviciosbaeza.com>
 * © 2016 ACSONE SA/NV (<http://acsone.eu>)
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
 */
odoo.define('document_url', function(require) {

    var core = require('web.core');
    var Sidebar = require('web.Sidebar');
    var ActionManager = require('web.ActionManager');

    var _t = core._t,
        QWeb = core.qweb;

    Sidebar.include({
        redraw: function() {
            var self = this;
            this._super.apply(this, arguments);
            self.$el.find('.oe_sidebar_add_attachment, .o_sidebar_add_attachment').after(QWeb.render('AddUrlDocumentItem', {widget: self}))
            self.$el.find('.oe_sidebar_add_url').on('click', function (e) {
                self.on_url_doc();
            });
        },
        on_url_doc: function() {
            var self = this;
            var view = self.getParent();
            var ids = ( view.fields_view.type != "form" )? view.groups.get_selection().ids : [ view.datarecord.id ];
            if( !_.isEmpty(ids) ){
                view.sidebar_eval_context().done(function (context) {
                    self.rpc("/web/action/load", { action_id: "document_url.action_ir_attachment_add_url" }).done(function(result) {
                        self.getParent().do_action(result, {
                            additional_context: {
                                'active_ids': ids,
                                'active_id': [ids[0]],
                                'active_model': view.dataset.model,
                            },
                        }); 
                    });
                });
            }
        },
    });

    ActionManager = ActionManager.include({
        ir_actions_act_close_wizard_and_reload_view: function (action, options) {
            if (!this.dialog) {
                options.on_close();
            }
            this.dialog_stop();
            this.inner_widget.views[this.inner_widget.active_view.type].controller.reload();
            return $.when();
        },
    });

});
