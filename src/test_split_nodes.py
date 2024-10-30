import unittest
import re
from textnode import TextNode, TextType
from split_nodes import split_nodes_delimiter, split_nodes_image, split_nodes_link


class TestSplitNodesImage(unittest.TestCase):
    def test_split_nodes_image(self):
        node = TextNode(
            "Here is an image of a cat looking at a mouse: ![A cat looks at a mouse.](https://img.freepik.com/premium-photo/cat-looking-mouse-table_865967-64208.jpg), isn't it cute?",
            TextType.TEXT,
        )
        test_result = split_nodes_image([node])
        expected_result = [
            TextNode("Here is an image of a cat looking at a mouse: ", TextType.TEXT),
            TextNode(
                "A cat looks at a mouse.",
                TextType.IMAGE,
                "https://img.freepik.com/premium-photo/cat-looking-mouse-table_865967-64208.jpg",
            ),
            TextNode(", isn't it cute?", TextType.TEXT),
        ]

        self.assertEqual(test_result, expected_result)


class TestSplitNodesLink(unittest.TestCase):
    def test_split_nodes_link(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev). Also, here is an image of a cat looking at a mouse: ![A cat looks at a mouse.](https://img.freepik.com/premium-photo/cat-looking-mouse-table_865967-64208.jpg), isn't it cute?",
            TextType.TEXT,
        )
        test_result = split_nodes_link([node])
        expected_result = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode(
                "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
            ),
            TextNode(
                ". Also, here is an image of a cat looking at a mouse: ![A cat looks at a mouse.](https://img.freepik.com/premium-photo/cat-looking-mouse-table_865967-64208.jpg), isn't it cute?",
                TextType.TEXT,
            ),
        ]

        self.assertEqual(test_result, expected_result)

        node = TextNode(
            "[to boot dev](https://www.boot.dev)",
            TextType.TEXT,
        )
        test_result = split_nodes_link([node])
        expected_result = [
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
        ]
        self.assertEqual(test_result, expected_result)


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
        node = TextNode("**bold** phrase **bold**", TextType.TEXT)
        delimiter = "**"
        text_type = TextType.BOLD
        expected_output = [
            TextNode("bold", TextType.BOLD),
            TextNode(" phrase ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
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

        # Multiple bold phrases
        node = TextNode("This is **bold** text **twice**.", TextType.TEXT)
        delimiter = "**"
        text_type = TextType.BOLD
        expected_output = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text ", TextType.TEXT),
            TextNode("twice", TextType.BOLD),
            TextNode(".", TextType.TEXT),
        ]
        result = split_nodes_delimiter([node], delimiter, text_type)
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
