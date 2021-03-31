from odoo.tests import common
from odoo.exceptions import AccessError


class TestDocumentPageApproval(common.TransactionCase):

    def setUp(self):
        super(TestDocumentPageApproval, self).setUp()
        self.page_obj = self.env['document.page']
        self.history_obj = self.env['document.page.history']
        # demo
        self.category1 = self.env.ref('document_page.demo_category1')
        self.page1 = self.env.ref('document_page.demo_page1')
        self.approver_gid = self.env.ref(
            'document_page_approval.group_document_approver_user')
        self.env.ref('base.user_root').write({
            'groups_id': [(4, self.approver_gid.id)],
        })
        self.user2 = self.env["res.users"].create(
            {
                "name": "Test user 2",
                "login": "Test user 2",
                "groups_id": [
                    (
                        6,
                        0,
                        [
                            self.env.ref("base.group_user").id,
                            self.approver_gid.id,
                        ],
                    )
                ],
            }
        )
        self.manager_gid = self.env.ref('document_page.group_document_manager')
        self.user_manager = self.env["res.users"].create(
            {
                "name": "Test document manager",
                "login": "Test document manager",
                "groups_id": [
                    (
                        6,
                        0,
                        [
                            self.env.ref("base.group_user").id,
                            self.manager_gid.id,
                        ],
                    )
                ],
            }
        )
        # demo_approval
        self.category2 = self.page_obj.create({
            'name': 'This category requires approval',
            'type': 'category',
            'approval_required': True,
            'approver_gid': self.approver_gid.id,
        })
        self.page2 = self.page_obj.create({
            'name': 'This page requires approval',
            'parent_id': self.category2.id,
            'content': 'This content will require approval',
        })

    def test_approval_required(self):
        page = self.page2
        self.assertTrue(page.is_approval_required)
        self.assertTrue(page.has_changes_pending_approval)
        self.assertEqual(len(page.history_ids), 0)

    def test_change_request_approve(self):
        page = self.page2
        chreq = self.history_obj.search([
            ('page_id', '=', page.id),
            ('state', '!=', 'approved')
        ])[0]

        # It should automatically be in 'to approve' state
        self.assertEqual(chreq.state, 'to approve')
        user_root = self.env.ref('base.user_root')
        self.assertTrue(user_root.partner_id.id in chreq.message_partner_ids.ids)
        self.assertTrue(self.user2.partner_id.id in chreq.message_partner_ids.ids)
        self.assertNotEqual(chreq.content, page.content)

        # who_am_i
        self.assertTrue(chreq.am_i_owner)
        self.assertTrue(chreq.am_i_approver)

        # approve
        chreq.action_approve()
        self.assertEqual(chreq.state, 'approved')
        self.assertEqual(chreq.content, page.content)

        # new changes should create change requests
        page.write({'content': 'New content'})
        self.assertNotEqual(page.content, 'New content')
        chreq = self.history_obj.search([
            ('page_id', '=', page.id),
            ('state', '!=', 'approved')
        ])[0]
        chreq.action_approve()
        self.assertEqual(page.content, 'New content')

    def test_change_request_auto_approve(self):
        page = self.page1
        self.assertFalse(page.is_approval_required)
        page.write({'content': 'New content'})
        self.assertEqual(page.content, 'New content')

    def test_change_request_from_scratch(self):
        page = self.page2

        # aprove everything
        self.history_obj.search([
            ('page_id', '=', page.id),
            ('state', '!=', 'approved')
        ]).action_approve()

        # new change request from scrath
        chreq = self.history_obj.create({
            'page_id': page.id,
            'summary': 'Changed something',
            'content': 'New content',
        })

        self.assertEqual(chreq.state, 'draft')
        self.assertNotEqual(page.content, chreq.content)
        self.assertNotEqual(page.approved_date, chreq.approved_date)
        self.assertNotEqual(page.approved_uid, chreq.approved_uid)

        chreq.action_to_approve()
        self.assertEqual(chreq.state, 'to approve')
        self.assertNotEqual(page.content, chreq.content)
        self.assertNotEqual(page.approved_date, chreq.approved_date)
        self.assertNotEqual(page.approved_uid, chreq.approved_uid)

        chreq.action_cancel()
        self.assertEqual(chreq.state, 'cancelled')
        self.assertNotEqual(page.content, chreq.content)
        self.assertNotEqual(page.approved_date, chreq.approved_date)
        self.assertNotEqual(page.approved_uid, chreq.approved_uid)

        chreq.action_draft()
        self.assertEqual(chreq.state, 'draft')
        self.assertNotEqual(page.content, chreq.content)
        self.assertNotEqual(page.approved_date, chreq.approved_date)
        self.assertNotEqual(page.approved_uid, chreq.approved_uid)

        chreq.action_approve()
        self.assertEqual(chreq.state, 'approved')
        self.assertEqual(page.content, chreq.content)
        self.assertEqual(page.approved_date, chreq.approved_date)
        self.assertEqual(page.approved_uid, chreq.approved_uid)

    def test_check_rules(self):
        page = self.page2
        # aprove everything
        self.history_obj.search([
            ('page_id', '=', page.id),
            ('state', '!=', 'approved')
        ]).action_approve()
        # new change request from scrath
        chreq = self.history_obj.create({
            'page_id': page.id,
            'summary': 'Changed something',
            'content': 'New content',
        })
        self.assertEqual(chreq.state, 'draft')
        chreq.action_to_approve()
        self.assertEqual(chreq.state, 'to approve')
        chreq.action_cancel()
        self.assertEqual(chreq.state, 'cancelled')
        chreq.sudo().action_draft()
        with self.assertRaises(AccessError):
            self.assertEqual(chreq.sudo(self.user2).state, 'draft')
        self.assertEqual(chreq.state, 'draft')
        self.assertEqual(chreq.sudo(self.user_manager).state, 'draft')
        chreq.action_approve()
        self.assertEqual(chreq.state, 'approved')

    def test_get_approvers_guids(self):
        """Get approver guids."""
        page = self.page2
        self.assertTrue(len(page.approver_group_ids) > 0)

    def test_get_page_url(self):
        """Test if page url exist."""
        pages = self.env['document.page.history'].search([])
        page = pages[0]
        self.assertIsNotNone(page.page_url)
