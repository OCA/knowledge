from odoo.tests import common


class TestDocumentContentSanitized(common.TransactionCase):
    def setUp(self):
        super(TestDocumentContentSanitized, self).setUp()
        self.page_obj = self.env["document.page"]
        self.category1 = self.env.ref("document_page.demo_category1")

    def test_page_content_sanitized(self):
        malicious_page = self.page_obj.create(
            {
                "name": "Malicious Page",
                "parent_id": self.category1.id,
                "content": "<p>Test content</p><script> alert(1)</script>",
            }
        )
        self.assertEqual(malicious_page.content, "<p>Test content</p>")

        malicious_page.write(
            {"content": "<p>Test content</p><script> alert(1)</script>"}
        )

        self.assertEqual(malicious_page.content, "<p>Test content</p>")
