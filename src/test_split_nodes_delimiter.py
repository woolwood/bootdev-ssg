import unittest
from textnode import TextNode, TextType
from split_nodes_delimiter import split_nodes_delimiter


class TestSplitNodesDelimiter(unittest.TestCase):

    def test_split_nodes_delimiter(self):

        # Bold phrase by itself
        node = TextNode("**bold**", TextType.TEXT)
        delimiter = "**"
        text_type = TextType.BOLD
        expected_output = [
            TextNode("bold", TextType.BOLD),
        ]
        result = split_nodes_delimiter([node], delimiter, text_type)

        self.assertEqual(result, expected_output)

        # Bolded phrase at start
        node = TextNode("**bold** phrase", TextType.TEXT)
        delimiter = "**"
        text_type = TextType.BOLD
        expected_output = [
            TextNode("bold", TextType.BOLD),
            TextNode(" phrase", TextType.TEXT),
        ]
        result = split_nodes_delimiter([node], delimiter, text_type)
        self.assertEqual(result, expected_output)

        # Check that empty TextNodes are not added to new_nodes
        nodes = [
            TextNode("", TextType.TEXT),
            TextNode("text", TextType.TEXT),
            TextNode("**bold**", TextType.TEXT),
        ]
        delimiter = "**"
        text_type = TextType.BOLD

        expected_output = [
            TextNode("text", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
        ]

        result = split_nodes_delimiter(nodes, delimiter, text_type)
        self.assertEqual(result, expected_output)

    def test_nested_delimiters(self):
        # Do not allow nested delimiters (wants an Exception).
        # In normal use bold text will be processed before italics, so
        # we are not checking for bold text inside of italic text using
        # italics processing.

        node = TextNode("**bold phrase with *italics* inside it.**", TextType.TEXT)
        delimiter = "**"
        text_type = TextType.BOLD

        with self.assertRaises(Exception) as e:
            split_nodes_delimiter([node], delimiter, text_type)
        self.assertIn("Nesting * inside of ** not allowed.", str(e.exception))

        # Test that it allows nesting inside of code tags.
        node = TextNode("`x = 2 * 6 * 3`", TextType.TEXT)
        delimiter = "`"
        text_type = TextType.CODE

        expected_output = [TextNode("x = 2 * 6 * 3", TextType.CODE)]
        result = split_nodes_delimiter([node], delimiter, text_type)
        self.assertEqual(result, expected_output)

    def test_consecutive_delimiters(self):

        node = TextNode("````code````", TextType.TEXT)
        delimiter = "`"
        text_type = TextType.CODE

        with self.assertRaises(Exception) as e:
            split_nodes_delimiter([node], delimiter, text_type)
        self.assertIn(
            "Empty field. Consecutive delimiter ` not allowed.", str(e.exception)
        )

    def test_unclosed_delimiter(self):

        node = TextNode("**bold phrase", TextType.TEXT)
        delimiter = "**"
        text_type = TextType.BOLD

        with self.assertRaises(Exception) as e:
            split_nodes_delimiter([node], delimiter, text_type)
        self.assertIn(
            "Invalid markdown code, closing delimiter ** not found.", str(e.exception)
        )


if __name__ == "__main__":
    unittest.main()
