import unittest
import re
from extract_markdown_uri import extract_markdown_images, extract_markdown_links


class TestExtractMarkdownUri(unittest.TestCase):
    def test_image_extraction(self):
        # Two image uri's formatted in markdown.abs
        text = "1) ![Jolly good!](jollygood.jpg). 2) ![A cat looks at a mouse.](https://img.freepik.com/premium-photo/cat-looking-mouse-table_865967-64208.jpg)"
        test_result = extract_markdown_images(text)
        expected_result = [
            ("Jolly good!", "jollygood.jpg"),
            (
                "A cat looks at a mouse.",
                "https://img.freepik.com/premium-photo/cat-looking-mouse-table_865967-64208.jpg",
            ),
        ]
        self.assertEqual(test_result, expected_result)

        # One URI with empty alt text.
        text = "1) ![](jollygood.jpg). 2) ![A cat looks at a mouse.](https://img.freepik.com/premium-photo/cat-looking-mouse-table_865967-64208.jpg)"
        test_result = extract_markdown_images(text)
        expected_result = [
            ("", "jollygood.jpg"),
            (
                "A cat looks at a mouse.",
                "https://img.freepik.com/premium-photo/cat-looking-mouse-table_865967-64208.jpg",
            ),
        ]
        self.assertEqual(test_result, expected_result)

    def test_link_extraction(self):
        text = "There are many search engines, but the most famous one is [Google](https://google.com). Privacy-oriented minds might prefer to use [DuckDuckGo](https://duckduckgo.com), or a region/language-specific engine such as the Russian [Yandex](https://yandex.com)."
        test_result = extract_markdown_links(text)
        expected_result = [
            ("Google", "https://google.com"),
            ("DuckDuckGo", "https://duckduckgo.com"),
            ("Yandex", "https://yandex.com"),
        ]
        self.assertEqual(test_result, expected_result)

    def test_ignore_img_link_extraction(self):
        text = "Image URI to ignore: ![A cat looks at a mouse.](https://img.freepik.com/premium-photo/cat-looking-mouse-table_865967-64208.jpg) and a link to capture: [Google](https://google.com)"
        test_result = extract_markdown_links(text)
        expected_result = [("Google", "https://google.com")]

        self.assertEqual(test_result, expected_result)


if __name__ == "__main__":
    unittest.main()
