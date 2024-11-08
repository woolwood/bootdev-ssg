import unittest
from generate_pages import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_extract_title(self):
        """Test extracting title from Markdown."""

        markdown = """# This is a h1 title.
With a body."""

        result = extract_title(markdown)
        expected_result = "This is a h1 title."

        self.assertEqual(result, expected_result)
if __name__ == "__main__":
    unittest.main()