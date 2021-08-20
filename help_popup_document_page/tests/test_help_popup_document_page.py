# -*- coding: utf-8 -*-
# © 2017 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp.tests.common import TransactionCase


class TestHelpPopupDocumentPage(TransactionCase):
    def test_help_popup_document_page(self):
        action = self.env.ref('base.action_res_users')
        self.assertEqual(
            action.enduser_help,
            '<p>This is the help for groups\nThis should be concatenated\n</p>'
        )
        self.assertEqual(
            action.advanced_help,
            '<p>This is the advanced help for groups</p>'
        )
