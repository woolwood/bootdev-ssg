from textnode import TextNode, TextType
from split_nodes import split_nodes_delimiter, split_nodes_image, split_nodes_link


def text_to_textnodes(text):
    # Construct a node around the the text
    node = TextNode(text, TextType.TEXT)

    # Chain the splitting functions
    formatted_links = split_nodes_link(split_nodes_image([node]))
    formatted_code = split_nodes_delimiter(formatted_links, "`", TextType.CODE)
    formatted_bold = split_nodes_delimiter(formatted_code, "**", TextType.BOLD)
    formatted_nodes = split_nodes_delimiter(formatted_bold, "*", TextType.ITALIC)

    return formatted_nodes
