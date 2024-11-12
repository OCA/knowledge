from odoo.tests import new_test_user

from odoo.addons.base.tests.common import BaseCommon


class TestDocumentPageApproval(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.page_obj = cls.env["document.page"]
        cls.history_obj = cls.env["document.page.history"]
        # demo
        cls.category1 = cls.env.ref("document_page.demo_category1")
        cls.page1 = cls.env.ref("document_page.demo_page1")
        cls.user2 = new_test_user(
            cls.env,
            login="test-user2",
            groups="base.group_user,document_page_approval.group_document_approver_user",
        )
        cls.approver_gid = cls.env.ref(
            "document_page_approval.group_document_approver_user"
        )
        # demo_approval
        cls.category2 = cls.page_obj.create(
            {
                "name": "This category requires approval",
                "type": "category",
                "approval_required": True,
                "approver_gid": cls.approver_gid.id,
            }
        )
        cls.page2 = cls.page_obj.create(
            {
                "name": "This page requires approval",
                "parent_id": cls.category2.id,
                "content": "This content will require approval",
            }
        )

    def test_approval_required(self):
        page = self.page2
        self.assertTrue(page.is_approval_required)
        self.assertTrue(page.has_changes_pending_approval)
        self.assertEqual(len(page.history_ids), 0)

    def test_change_request_approve(self):
        page = self.page2
        chreq = self.history_obj.search(
            [("page_id", "=", page.id), ("state", "!=", "approved")]
        )[0]

        # It should automatically be in 'to approve' state
        self.assertEqual(chreq.state, "to approve")
        user_admin = self.env.ref("base.user_admin")
        self.assertTrue(user_admin.partner_id.id in chreq.message_partner_ids.ids)
        self.assertTrue(self.user2.partner_id.id in chreq.message_partner_ids.ids)

        # Needed to compute calculated fields
        page.invalidate_model()
        self.assertNotEqual(chreq.content, page.content)

        # who_am_i
        self.assertTrue(chreq.am_i_owner)
        self.assertTrue(chreq.am_i_approver)

        # approve
        chreq.action_approve()
        self.assertEqual(chreq.state, "approved")
        self.assertEqual(chreq.content, page.content)

        # new changes should create change requests
        page.write({"content": "New content"})
        # Needed to compute calculated fields
        page.invalidate_model()
        self.assertNotEqual(page.content, "New content")
        chreq = self.history_obj.search(
            [("page_id", "=", page.id), ("state", "!=", "approved")]
        )[0]
        chreq.action_approve()
        self.assertEqual(page.content, "New content")

    def test_change_request_auto_approve(self):
        page = self.page1
        self.assertFalse(page.is_approval_required)
        page.write({"content": "New content"})
        self.assertEqual(page.content, "New content")

    def test_change_request_from_scratch(self):
        page = self.page2

        # aprove everything
        self.history_obj.search(
            [("page_id", "=", page.id), ("state", "!=", "approved")]
        ).action_approve()

        # new change request from scrath
        chreq = self.history_obj.create(
            {
                "page_id": page.id,
                "summary": "Changed something",
                "content": "New content",
            }
        )

        self.assertEqual(chreq.state, "draft")
        self.assertNotEqual(page.content, chreq.content)
        self.assertNotEqual(page.approved_date, chreq.approved_date)
        self.assertNotEqual(page.approved_uid, chreq.approved_uid)

        chreq.action_to_approve()
        self.assertEqual(chreq.state, "to approve")
        self.assertNotEqual(page.content, chreq.content)
        self.assertNotEqual(page.approved_date, chreq.approved_date)
        self.assertNotEqual(page.approved_uid, chreq.approved_uid)

        chreq.action_cancel()
        self.assertEqual(chreq.state, "cancelled")
        self.assertNotEqual(page.content, chreq.content)
        self.assertNotEqual(page.approved_date, chreq.approved_date)
        self.assertNotEqual(page.approved_uid, chreq.approved_uid)

        chreq.action_draft()
        self.assertEqual(chreq.state, "draft")
        self.assertNotEqual(page.content, chreq.content)
        self.assertNotEqual(page.approved_date, chreq.approved_date)
        self.assertNotEqual(page.approved_uid, chreq.approved_uid)

        chreq.action_approve()
        self.assertEqual(chreq.state, "approved")
        self.assertEqual(page.content, chreq.content)
        self.assertEqual(page.approved_date, chreq.approved_date)
        self.assertEqual(page.approved_uid, chreq.approved_uid)

    def test_get_approvers_guids(self):
        """Get approver guids."""
        page = self.page2
        self.assertTrue(len(page.approver_group_ids) > 0)

    def test_get_page_url(self):
        """Test if page url exist."""
        pages = self.env["document.page.history"].search([])
        page = pages[0]
        self.assertIsNotNone(page.page_url)
