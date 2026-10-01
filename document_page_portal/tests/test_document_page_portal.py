# Copyright 2020 - TODAY, Marcel Savegnago - Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import odoo.tests


@odoo.tests.tagged("post_install", "-at_install")
class TestPortalDocumentPage(odoo.tests.HttpCase):
    def test_01_document_page_portal_tour(self):
        # Create a public document
        self.env["document.page"].create(
            {
                "name": "Test Public Page 1",
                "content": "Test content",
                "is_public": True,
            }
        )
        self.start_tour("/my", "document_page_portal_tour", login="portal")

    def test_02_document_page_portal_search_tour(self):
        # Create a public document
        self.env["document.page"].create(
            {
                "name": "Test Public Page 1",
                "content": "Test content",
                "is_public": True,
            }
        )
        self.start_tour(
            "/my/knowledge/documents",
            "document_page_portal_search_tour",
            login="portal",
        )


@odoo.tests.tagged("post_install", "-at_install")
class TestPortalDocumentPageController(odoo.tests.HttpCase):
    """HTTP-level tests for the controller branches the browser tours do not
    exercise: the access-denied/missing-record redirect in
    ``document_pages_followup`` and the date-range filter of the document
    list. These use ``url_open`` (no browser), so they add coverage without
    launching Chrome.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.portal_user = (
            cls.env["res.users"]
            .with_context(no_reset_password=True)
            .create(
                {
                    "name": "Portal Test User",
                    "login": "portal_test_user",
                    "password": "portal_test_user",
                    "email": "portal_test_user@example.com",
                    "groups_id": [(6, 0, [cls.env.ref("base.group_portal").id])],
                }
            )
        )
        # Public page: a portal user may read it (is_public rule leaf).
        cls.public_page = cls.env["document.page"].create(
            {
                "name": "Portal Public Page",
                "content": "Public content",
                "is_public": True,
            }
        )
        # Public page that must NOT match the search term below: without it,
        # a domain that matches everything is indistinguishable from a
        # working filter.
        cls.other_public_page = cls.env["document.page"].create(
            {
                "name": "Zebra Handbook",
                "content": "Stripey quadruped notes",
                "is_public": True,
            }
        )
        # Private content page the portal user does not follow: no access.
        cls.private_page = cls.env["document.page"].create(
            {
                "name": "Portal Private Page",
                "content": "Private content",
                "is_public": False,
            }
        )

    def test_03_followup_access_error_redirects(self):
        """A portal user without access to a page is redirected to /my."""
        self.authenticate("portal_test_user", "portal_test_user")
        response = self.url_open(
            f"/knowledge/document/{self.private_page.id}",
            allow_redirects=False,
        )
        self.assertEqual(response.status_code, 303)
        self.assertTrue(response.headers.get("Location", "").endswith("/my"))

    def test_04_followup_missing_record_redirects(self):
        """A request for a non-existent page is redirected to /my."""
        self.authenticate("portal_test_user", "portal_test_user")
        missing_id = self.public_page.id + 1000000
        response = self.url_open(
            f"/knowledge/document/{missing_id}",
            allow_redirects=False,
        )
        self.assertEqual(response.status_code, 303)
        self.assertTrue(response.headers.get("Location", "").endswith("/my"))

    def test_05_document_list_date_filter(self):
        """The date_begin/date_end filter narrows the portal document list."""
        self.authenticate("portal_test_user", "portal_test_user")
        # A range entirely in the past excludes the just-created page.
        past = self.url_open(
            "/my/knowledge/documents?date_begin=2000-01-01&date_end=2000-12-31"
        )
        self.assertEqual(past.status_code, 200)
        self.assertNotIn("Portal Public Page", past.text)
        # A range covering today includes it.
        present = self.url_open(
            "/my/knowledge/documents?date_begin=2000-01-01&date_end=2999-12-31"
        )
        self.assertEqual(present.status_code, 200)
        self.assertIn("Portal Public Page", present.text)

    def test_06_document_list_search_filter(self):
        """The search term narrows the portal document list."""
        self.authenticate("portal_test_user", "portal_test_user")
        res = self.url_open("/my/knowledge/documents?search=Stripey&search_in=content")
        self.assertEqual(res.status_code, 200)
        # "Stripey" appears only in the content of the Zebra page.
        self.assertIn("Zebra Handbook", res.text)
        self.assertNotIn("Portal Public Page", res.text)

    def test_07_searchbar_label_is_markup(self):
        """The searchbar label renders as markup, not as escaped text."""
        self.authenticate("portal_test_user", "portal_test_user")
        res = self.url_open("/my/knowledge/documents")
        self.assertEqual(res.status_code, 200)
        self.assertIn('<span class="nolabel"> (in Content)</span>', res.text)
        self.assertNotIn("Search &lt;span", res.text)

    def test_08_portal_home_card_icon(self):
        """The portal home card points at an icon that is actually served."""
        self.authenticate("portal_test_user", "portal_test_user")
        icon = "/document_page_portal/static/src/img/knowledge.svg"
        home = self.url_open("/my/home")
        self.assertEqual(home.status_code, 200)
        self.assertIn(icon, home.text)
        self.assertEqual(self.url_open(icon).status_code, 200)
