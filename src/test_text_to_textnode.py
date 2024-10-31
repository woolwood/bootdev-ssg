import unittest
from textnode import TextNode, TextType
from text_to_textnode import text_to_textnodes


class TestTextToTextnode(unittest.TestCase):
    def test_text_to_textnode(self):
        input_text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result = text_to_textnodes(input_text)
        expected_output = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]

    def test_nested_delimiters(self):
        input_text = "**bold phrase with *italics* inside it.**"

        with self.assertRaises(Exception) as e:
            text_to_textnodes(input_text)
        self.assertIn("Nesting * inside of ** not allowed.", str(e.exception))

        # Test that it allows nesting inside of code tags.
        input_text = "`x = 2 * 6 * 3`"

        expected_output = [TextNode("x = 2 * 6 * 3", TextType.CODE)]
        result = text_to_textnodes(input_text)
        self.assertEqual(result, expected_output)

    def test_consecutive_delimiters(self):
        input_text = "Check out this wrong ````code````"

        with self.assertRaises(Exception) as e:
            text_to_textnodes(input_text)
        self.assertIn("Empty field. Consecutive delimiter ` not allowed.", str(e.exception))

    def test_unclosed_delimiter(self):
        input_text = "**bold phrase"

        with self.assertRaises(Exception) as e:
            text_to_textnodes(input_text)
        self.assertIn("Invalid markdown code, closing delimiter ** not found.", str(e.exception))


if __name__ == "__main__":
    unittest.main()
