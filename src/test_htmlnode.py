import unittest
from htmlnode import HTMLNode, ParentNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        node = HTMLNode(props=props)
        self.assertEqual(
            node.props_to_html(), ' href="https://www.google.com" target="_blank"'
        )

    def test_children(self):
        node = HTMLNode(children="kids")
        self.assertEqual(node.children, "kids")

    def test_repr(self):
        node = HTMLNode()
        self.assertEqual(
            repr(node), "tag = None, value = None, children = None, props = None"
        )


class TestParentNode(unittest.TestCase):
    def test_to_html(self):
        children = [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
        ]
        pnode = ParentNode(
            "div",
            [
                LeafNode("a", "Click me!", {"href": "https://www.google.com"}),
            ],
        )

        pnode_with_list = ParentNode("div", children)

        self.assertEqual(
            pnode.to_html(), '<div><a href="https://www.google.com">Click me!</a></div>'
        )

        self.assertEqual(
            pnode_with_list.to_html(), "<div><b>Bold text</b>Normal text</div>"
        )


class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        node2 = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(
            node.to_html(), '<a href="https://www.google.com">Click me!</a>'
        )
        self.assertEqual(node2.to_html(), "<p>This is a paragraph of text.</p>")

    # def test_children(self):
    #     node = LeafNode(value="This is a test", children="child tag")
    #     self.assertRaises()

    # def test_no_value(self):
    #     node = LeafNode("p")


if __name__ == "__main__":
    unittest.main()
