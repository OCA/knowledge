# Copyright 2026 NuoBiT Solutions SL - Deniz Gallo <dgallo@nuobit.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from lxml import etree

from odoo import Command
from odoo.exceptions import UserError
from odoo.tests import new_test_user
from odoo.tools.safe_eval import safe_eval

from odoo.addons.base.tests.common import BaseCommon


class TestDocumentPageHistory(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.history_obj = cls.env["document.page.history"]
        cls.page_approvers = cls.env["res.groups"].create({"name": "Page approvers"})
        cls.owner = new_test_user(
            cls.env,
            login="test_owner",
            groups="document_knowledge.group_document_user,"
            "document_page.group_document_editor",
            name="Test owner",
        )
        cls.approver = new_test_user(
            cls.env,
            login="test_approver",
            groups="document_page_approval.group_document_approver_user",
            name="Test approver",
        )
        cls.approver.write({"group_ids": [Command.link(cls.page_approvers.id)]})
        cls.other_approver = new_test_user(
            cls.env,
            login="test_other_approver",
            groups="document_page_approval.group_document_approver_user",
            name="Test other approver",
        )
        cls.manager = new_test_user(
            cls.env,
            login="test_manager",
            groups="document_page.group_document_manager",
            name="Test manager",
        )
        category = cls.env["document.page"].create(
            {
                "name": "This category requires approval",
                "type": "category",
                "approval_required": True,
                "approver_gid": cls.page_approvers.id,
            }
        )
        cls.page = cls.env["document.page"].create(
            {"name": "This page requires approval", "parent_id": category.id}
        )

    def _create_change_request(self, user):
        return self.history_obj.with_user(user).create(
            {
                "page_id": self.page.id,
                "summary": "Changed something",
                "content": "<p>New content</p>",
            }
        )

    def _with_user(self, record, user):
        # a request of that user starts with an empty cache
        self.env.invalidate_all()
        return record.with_user(user)

    def _visible_buttons(self, record, string):
        """Methods of the buttons labelled `string` that the record's user sees."""
        arch = record.get_views([(False, "form")])["views"]["form"]["arch"]
        values = {
            "am_i_owner": record.am_i_owner,
            "am_i_approver": record.am_i_approver,
            "is_approval_required": record.is_approval_required,
            "state": record.state,
        }
        names = []
        for button in etree.fromstring(arch).iter("button"):
            if button.get("string") == string and not safe_eval(
                button.get("invisible", "False"), values
            ):
                names.append(button.get("name"))
        return names

    def _click(self, record, string):
        names = self._visible_buttons(record, string)
        self.assertEqual(len(names), 1, names)
        return getattr(record, names[0])()

    def test_manager_owner_back_to_draft_pending(self):
        """Ensure a manager sends their own pending request back to draft"""
        chreq = self._create_change_request(self.manager)
        chreq.action_to_approve()
        self._click(chreq, "Back to draft")
        self.assertEqual(chreq.state, "draft")
        self.assertIn("has been cancelled by Test manager.", chreq.message_ids[0].body)

    def test_manager_back_to_draft_pending(self):
        """Ensure a manager sends someone else's pending request back to draft"""
        chreq = self._create_change_request(self.owner)
        chreq.action_to_approve()
        chreq = self._with_user(chreq, self.manager)
        self._click(chreq, "Back to draft")
        self.assertEqual(chreq.state, "draft")
        self.assertIn("has been cancelled by Test manager.", chreq.message_ids[0].body)

    def test_other_approver_no_back_to_draft_pending(self):
        """Ensure Back to draft is hidden from who is neither owner nor approver"""
        chreq = self._create_change_request(self.owner)
        chreq.action_to_approve()
        self.assertEqual(chreq.state, "to approve")
        chreq = self._with_user(chreq, self.other_approver)
        self.assertEqual(self._visible_buttons(chreq, "Back to draft"), [])

    def test_manager_back_to_draft_cancelled(self):
        """Ensure Back to draft still reopens a cancelled request"""
        chreq = self._create_change_request(self.manager)
        chreq.action_to_approve()
        chreq.action_cancel()
        self._click(chreq, "Back to draft")
        self.assertEqual(chreq.state, "draft")

    def test_other_approver_no_cancel_and_draft_pending(self):
        """Ensure who is neither owner nor approver cannot cancel and reopen"""
        chreq = self._create_change_request(self.owner)
        chreq.action_to_approve()
        chreq = self._with_user(chreq, self.other_approver)
        with self.assertRaises(UserError) as error:
            chreq.action_cancel_and_draft()
        self.assertEqual(
            error.exception.args[0],
            "You are not authorized to do this.\n"
            "Only owners or approvers can cancel Change Requests.",
        )
        self.assertEqual(chreq.state, "to approve")

    def test_owner_no_cancel_approved(self):
        """Ensure an approved request cannot be cancelled"""
        chreq = self._create_change_request(self.owner)
        chreq.action_to_approve()
        self._with_user(chreq, self.approver).action_approve()
        chreq = self._with_user(chreq, self.owner)
        with self.assertRaises(UserError) as error:
            chreq.action_cancel()
        self.assertEqual(
            error.exception.args[0],
            "Can't cancel change requests in 'approved' state.",
        )
        self.assertEqual(chreq.state, "approved")

    def test_owner_no_cancel_cancelled(self):
        """Ensure a cancelled request cannot be cancelled again"""
        chreq = self._create_change_request(self.owner)
        chreq.action_cancel()
        with self.assertRaises(UserError) as error:
            chreq.action_cancel()
        self.assertEqual(
            error.exception.args[0],
            "Can't cancel change requests in 'cancelled' state.",
        )
        self.assertEqual(chreq.state, "cancelled")

    def test_other_approver_no_cancel_pending(self):
        """Ensure who is neither owner nor approver cannot cancel"""
        chreq = self._create_change_request(self.owner)
        chreq.action_to_approve()
        chreq = self._with_user(chreq, self.other_approver)
        with self.assertRaises(UserError) as error:
            chreq.action_cancel()
        self.assertEqual(
            error.exception.args[0],
            "You are not authorized to do this.\n"
            "Only owners or approvers can cancel Change Requests.",
        )
        self.assertEqual(chreq.state, "to approve")

    def test_owner_cancel_draft(self):
        """Ensure the owner cancels their draft request"""
        chreq = self._create_change_request(self.owner)
        self._click(chreq, "Cancel")
        self.assertEqual(chreq.state, "cancelled")
        self.assertIn("has been cancelled by Test owner.", chreq.message_ids[0].body)

    def test_owner_cancel_pending(self):
        """Ensure the owner cancels their pending request"""
        chreq = self._create_change_request(self.owner)
        chreq.action_to_approve()
        self._click(chreq, "Cancel")
        self.assertEqual(chreq.state, "cancelled")
        self.assertIn("has been cancelled by Test owner.", chreq.message_ids[0].body)

    def test_approver_cancel_pending(self):
        """Ensure an approver cancels a pending request"""
        chreq = self._create_change_request(self.owner)
        chreq.action_to_approve()
        chreq = self._with_user(chreq, self.approver)
        self._click(chreq, "Cancel")
        self.assertEqual(chreq.state, "cancelled")
        self.assertIn("has been cancelled by Test approver.", chreq.message_ids[0].body)
