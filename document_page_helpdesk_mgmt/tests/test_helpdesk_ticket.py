# Copyright 2026 - TODAY, Cristiano Mafra Junior <cristiano.mafra@escodoo.com.br>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import common


class TestHelpdeskTicket(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.Page = cls.env["document.page"]
        cls.Ticket = cls.env["helpdesk.ticket"]
        cls.Team = cls.env["helpdesk.ticket.team"]
        cls.default_page = cls.Page.create({"name": "My page"})
        cls.default_team = cls.Team.create({"name": "Team A"})

    def test_page_count(self):
        ticket = self.Ticket.create(
            {
                "name": "Ticket A",
                "description": "Ticket description",
                "team_id": self.default_team.id,
            }
        )

        self.assertEqual(
            ticket.document_page_count, 0, "Initial page count should be zero"
        )

        self.default_page.helpdesk_ticket_ids = [(4, ticket.id)]
        ticket._compute_document_page_count()

        self.assertEqual(
            ticket.document_page_count,
            1,
            "After attaching ticket to document the page count should be one",
        )
        self.assertIn(
            self.default_page,
            ticket.document_page_ids,
            "The page should be in the list of document pages for ticket",
        )
