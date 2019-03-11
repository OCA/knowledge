/* Copyright 2014 Serv. Tecnol. Avanzados (http://www.serviciosbaeza.com)
 *                      Pedro M. Baeza <pedro.baeza@serviciosbaeza.com>
 * Copyright 2016 ACSONE SA/NV (<http://acsone.eu>)
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
 */
odoo.define('document_url', function (require) {

    var core = require('web.core');
    var Sidebar = require('web.Sidebar');
    var ActionManager = require('web.ActionManager');
    var Context = require('web.Context');
    var pyeval = require('web.pyeval');

    var _t = core._t,
        QWeb = core.qweb;

    Sidebar.include({
        _redraw: function () {
            var self = this;
            this._super.apply(this, arguments);
            self.$el.find("a[href]").attr('target', '_blank');
            self.$el
                .find('.oe_sidebar_add_attachment, .o_sidebar_add_attachment')
                .after(QWeb.render('AddUrlDocumentItem', {widget: self}));
            self.$el.find('.o_sidebar_add_url').on('click', function (e) {
                self.on_url_doc();
            });
        },
        on_url_doc: function (event) {

            var self = this;
            var env = self.env;
            var view = self.getParent();
            var ids = self.env.activeIds;
            if (!_.isEmpty(ids)) {
                var activeIdsContext = {
                    active_id: env.activeIds[0],
                    active_ids: env.activeIds,
                    active_model: env.model,
                };
                if (env.domain) {
                    activeIdsContext.active_domain = env.domain;
                }
                var context = new Context(env.context, activeIdsContext);
                context = pyeval.eval('context', context);
                self._rpc({
                    route: "/web/action/load",
                    params: {
                        action_id: "document_url.action_ir_attachment_add_url",
                        context: context,
                    },
                }).done(function (result) {
                    self.getParent().do_action(result, {
                        additional_context: {
                            'active_ids': ids,
                            'active_id': [ids[0]],
                            'active_model': env.model,
                        },
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
