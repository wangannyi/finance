import unittest

from finance_app.crawler import extract_document


class CrawlerTests(unittest.TestCase):
    def test_extract_document_returns_url_title_and_text(self):
        html = """
        <html>
          <head>
            <title>AI Optical Transceiver News</title>
            <meta name="description" content="CPO optical interconnect demand rises">
          </head>
          <body><h1>Co-packaged optics in AI data centers</h1></body>
        </html>
        """

        document = extract_document("https://example.com/news", html)

        self.assertEqual(document["url"], "https://example.com/news")
        self.assertEqual(document["title"], "AI Optical Transceiver News")
        self.assertIn("Co-packaged optics", document["text"])
        self.assertIsNone(document["error"])


if __name__ == "__main__":
    unittest.main()
