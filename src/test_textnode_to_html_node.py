import unittest
from textnode import TextNode, TextType
from htmlnode import LeafNode
from textnode_to_html_node import textnode_to_html_node


class TestTextNodeToHtmlNode(unittest.TestCase):
    def test_bold_node_to_html(self):
        """Test BOLD TextType conversion."""
        textnode = TextNode("This is some text.", TextType.BOLD)

        self.assertEqual(LeafNode("b", "This is some text."), textnode_to_html_node(textnode))

    def test_image_node_to_html(self):
        """Test IMAGE TextType conversion."""

        image_node = TextNode("This is some text.", TextType.IMAGE, "http://google.com/")
        wanted_image_node = LeafNode(
            "img", "", {"src": "http://google.com/", "alt": "This is some text."}
        )
        self.assertEqual(textnode_to_html_node(image_node), wanted_image_node)

    def test_link_node_to_html(self):
        """Test LINK TextType conversion."""

        link_node = TextNode("Anchor text", TextType.LINK, "http://google.com/")
        wanted_link_node = LeafNode("a", "Anchor text", {"href": "http://google.com/"})
        self.assertEqual(textnode_to_html_node(link_node), wanted_link_node)


if __name__ == "__main__":
    unittest.main()
