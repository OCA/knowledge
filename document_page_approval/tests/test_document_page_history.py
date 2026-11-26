# Copyright 2026 NuoBiT Solutions SL - Deniz Gallo <dgallo@nuobit.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import json

from lxml import etree

from odoo.tests import common


class TestDocumentPageHistory(common.TransactionCase):
    def setUp(self):
        super(TestDocumentPageHistory, self).setUp()
        self.history_obj = self.env["document.page.history"]
        approver_gid = self.env.ref(
            "document_page_approval.group_document_approver_user"
        )
        self.page_approvers = self.env["res.groups"].create({"name": "Page approvers"})
        self.owner = self.env["res.users"].create(
            {
                "name": "Test owner",
                "login": "Test owner",
                "email": "owner@example.com",
                "groups_id": [
                    (
                        6,
                        0,
                        [
                            self.env.ref("base.group_user").id,
                            self.env.ref("document_page.group_document_editor").id,
                        ],
                    )
                ],
            }
        )
        self.approver = self.env["res.users"].create(
            {
                "name": "Test approver",
                "login": "Test approver",
                "email": "approver@example.com",
                "groups_id": [
                    (
                        6,
                        0,
                        [
                            self.env.ref("base.group_user").id,
                            approver_gid.id,
                            self.page_approvers.id,
                        ],
                    )
                ],
            }
        )
        self.other_approver = self.env["res.users"].create(
            {
                "name": "Test other approver",
                "login": "Test other approver",
                "email": "other.approver@example.com",
                "groups_id": [
                    (6, 0, [self.env.ref("base.group_user").id, approver_gid.id])
                ],
            }
        )
        category = self.env["document.page"].create(
            {
                "name": "This category requires approval",
                "type": "category",
                "approval_required": True,
                "approver_gid": self.page_approvers.id,
            }
        )
        self.page = self.env["document.page"].create(
            {"name": "This page requires approval", "parent_id": category.id}
        )

    def _create_change_request(self):
        return self.history_obj.with_user(self.owner).create(
            {
                "page_id": self.page.id,
                "summary": "Changed something",
                "content": "<p>New content</p>",
            }
        )

    def _with_user(self, record, user):
        # am_i_owner and am_i_approver depend on the user without declaring it
        # (no depends_context): forget the values computed for the previous one
        record.invalidate_cache()
        return record.with_user(user)

    def _visible_buttons(self, record, string):
        """Methods of the buttons labelled `string` that the record's user sees."""
        view = record.fields_view_get(view_type="form")
        names = []
        for button in etree.fromstring(view["arch"]).iter("button"):
            invisible = json.loads(button.get("modifiers", "{}")).get("invisible")
            if isinstance(invisible, list):
                invisible = bool(record.filtered_domain(invisible))
            if button.get("string") == string and not invisible:
                names.append(button.get("name"))
        return names

    def _click(self, record, string):
        names = self._visible_buttons(record, string)
        self.assertEqual(len(names), 1, names)
        return getattr(record, names[0])()

    def test_owner_back_to_draft_pending(self):
        chreq = self._create_change_request()
        chreq.action_to_approve()
        self._click(chreq, "Back to draft")
        self.assertEqual(chreq.state, "draft")
        self.assertIn("has been cancelled by Test owner.", chreq.message_ids[0].body)

    def test_approver_back_to_draft_pending(self):
        chreq = self._create_change_request()
        chreq.action_to_approve()
        chreq = self._with_user(chreq, self.approver)
        self._click(chreq, "Back to draft")
        chreq = self._with_user(chreq, self.owner)
        self.assertEqual(chreq.state, "draft")
        self.assertIn("has been cancelled by Test approver.", chreq.message_ids[0].body)

    def test_other_approver_no_back_to_draft_pending(self):
        chreq = self._create_change_request()
        chreq.action_to_approve()
        self.assertEqual(chreq.state, "to approve")
        chreq = self._with_user(chreq, self.other_approver)
        self.assertEqual(self._visible_buttons(chreq, "Back to draft"), [])

    def test_owner_back_to_draft_cancelled(self):
        chreq = self._create_change_request()
        chreq.action_to_approve()
        chreq.action_cancel()
        self._click(chreq, "Back to draft")
        self.assertEqual(chreq.state, "draft")
