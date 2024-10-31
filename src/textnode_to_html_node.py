from textnode import TextNode, TextType
from htmlnode import LeafNode


def textnode_to_html_node(textnode):
    match textnode.text_type:
        case TextType.TEXT:
            return LeafNode(None, textnode.text)

        case TextType.BOLD:
            return LeafNode("b", textnode.text)

        case TextType.CODE:
            return LeafNode("code", textnode.text)

        case TextType.ITALIC:
            return LeafNode("i", textnode.text)

        case TextType.LINK:
            return LeafNode("a", textnode.text, {"href": textnode.url})

        case TextType.IMAGE:
            return LeafNode("img", "", {"src": textnode.url, "alt": textnode.text})

        case _:
            raise ValueError(f"Invalid TextType: {textnode.text_type}")
