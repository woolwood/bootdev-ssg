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

    def test_extract_title_hashtag(self):
        """Test extracting title with leading # from Markdown."""

        markdown = """# #This is a h1 title.
With a body."""

        result = extract_title(markdown)
        expected_result = "#This is a h1 title."

        self.assertEqual(result, expected_result)

    def test_extract_title_no_heading(self):
        """Test extracting title from Markdown without header"""

        markdown = "This is not a h1 title."

        with self.assertRaises(Exception) as e:
            extract_title(markdown)
        self.assertIn("Document must have h1 heading.", str(e.exception))

    def test_extract_title_wrong_heading(self):
        """Test extracting title from Markdown without header"""

        markdown = "## This is not a h1 title."

        with self.assertRaises(Exception) as e:
            extract_title(markdown)
        self.assertIn("Document must have h1 heading.", str(e.exception))

    def test_extract_title_glued_heading(self):
        """Test extracting title from Markdown without header"""

        markdown = "#This is not a h1 title."

        with self.assertRaises(Exception) as e:
            extract_title(markdown)
        self.assertIn("Document must have h1 heading.", str(e.exception))


if __name__ == "__main__":
    unittest.main()
