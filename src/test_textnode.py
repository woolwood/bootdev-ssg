import unittest
from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        """Test equality of TextNode with BOLD TextType"""
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_url(self):
        """Test equality of TextNode with LINK TextType, with a URL."""
        node = TextNode("This is a text node", TextType.LINK, "https://google.com")
        node2 = TextNode("This is a text node", TextType.LINK, "https://google.com")
        self.assertEqual(node, node2)

    def test_different_text(self):
        """Test inequality when text is different."""
        node1 = TextNode("Text node 1", TextType.TEXT)
        node2 = TextNode("Text node 2", TextType.TEXT)
        self.assertNotEqual(node1, node2)

    def test_different_type(self):
        """Test inequality when text types are different."""
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node1, node2)

    def test_different_url(self):
        """Test inequality when URLs are different."""
        node1 = TextNode("This is a text node", TextType.LINK, "https://example.com")
        node2 = TextNode("This is a text node", TextType.LINK, "https://another.com")
        self.assertNotEqual(node1, node2)


if __name__ == "__main__":
    unittest.main()
