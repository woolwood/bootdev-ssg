import unittest
from htmlnode import HTMLNode, ParentNode, LeafNode
from markdown_to_html_node import markdown_to_html_node, block_to_htmlnode
from text_to_textnode import text_to_textnodes


class TestMarkdownToHtmlConversion(unittest.TestCase):
    def test_quote_conversion(self):
        markdown = "> This is a quote."
        expected_node = ParentNode("blockquote", [LeafNode(None, "This is a quote.")])
        result_node = block_to_htmlnode(markdown)
        self.assertEqual(result_node, expected_node)

    def test_unordered_list_conversion(self):
        markdown = "* Item 1\n* Item 2"
        expected_node = ParentNode(
            "ul",
            [
                ParentNode("li", [LeafNode(None, "Item 1")]),
                ParentNode("li", [LeafNode(None, "Item 2")]),
            ],
        )
        result_node = block_to_htmlnode(markdown)
        self.assertEqual(result_node, expected_node)

    def test_ordered_list_conversion(self):
        markdown = "1. First item\n2. Second item"
        expected_node = ParentNode(
            "ol",
            [
                ParentNode("li", [LeafNode(None, "First item")]),
                ParentNode("li", [LeafNode(None, "Second item")]),
            ],
        )
        result_node = block_to_htmlnode(markdown)
        self.assertEqual(result_node, expected_node)

    def test_code_block_conversion(self):
        markdown = """```\ndef test():\n    pass\n```"""
        expected_node = ParentNode(
            "pre", [ParentNode("code", [LeafNode(None, """\ndef test():\n    pass\n""")])]
        )
        result_node = block_to_htmlnode(markdown)
        self.assertEqual(result_node, expected_node)

    def test_heading_conversion(self):
        markdown = "## Heading Level 2"
        expected_node = ParentNode("h2", [LeafNode(None, "Heading Level 2")])
        result_node = block_to_htmlnode(markdown)
        self.assertEqual(result_node, expected_node)

    def test_heading_conversion_pound(self):
        markdown = "# #Hashtag in heading"
        expected_node = ParentNode("h1", [LeafNode(None, "#Hashtag in heading")])
        result_node = block_to_htmlnode(markdown)
        self.assertEqual(result_node, expected_node)
        

    def test_paragraph_conversion(self):
        markdown = "This is a simple paragraph."
        expected_node = ParentNode("p", [LeafNode(None, "This is a simple paragraph.")])
        result_node = block_to_htmlnode(markdown)
        self.assertEqual(result_node, expected_node)

    def test_combined_markdown(self):
        markdown = (
            "> Blockquote\n\n1. Ordered item\n\n* Unordered item\n\n```\nCode *block* block\n```"
        )
        expected_node = HTMLNode(
            "div",
            children=[
                ParentNode("blockquote", [LeafNode(None, "Blockquote")]),
                ParentNode("ol", [ParentNode("li", [LeafNode(None, "Ordered item")])]),
                ParentNode("ul", [ParentNode("li", [LeafNode(None, "Unordered item")])]),
                ParentNode("pre", [ParentNode("code", [LeafNode(None, "\nCode *block* block\n")])]),
            ],
        )
        result_node = markdown_to_html_node(markdown)
        self.assertEqual(result_node, expected_node)

    def test_inline_and_block_md(self):
        markdown = """## Hypoheader
This is a hypothetical raw markdown document which contains **bold** and *italics* text."""

        expected_node = HTMLNode(
            "div",
            children=[
                ParentNode("h2", [LeafNode(None, "Hypoheader")]),
                ParentNode(
                    "p",
                    [
                        LeafNode(
                            None, "This is a hypothetical raw markdown document which contains "
                        ),
                        LeafNode("b", "bold"),
                        LeafNode(None, " and "),
                        LeafNode("i", "italics"),
                        LeafNode(None, " text."),
                    ],
                ),
            ],
        )


if __name__ == "__main__":
    unittest.main()
