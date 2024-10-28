from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """
    Takes a list of 'old nodes', delimiter and text type,
    returns new list of nodes split by text type.
    """

    def splitter(node, delimiter, text_type):
        if delimiter not in node.text:
            if node.text:
                new_nodes.append(node)
            return
        if node.text.count(delimiter) % 2 != 0:
            raise Exception(
                "Invalid markdown code, closing delimiter {delimiter} not found."
            )
        delimiters = ["*", "**"]
        node_parts = node.text.split(delimiter, 2)
        if node_parts[0]:
            new_nodes.append(TextNode(node_parts[0], TextType.TEXT))
        if text_type != TextType.CODE:
            for d in delimiters:
                if d in node_parts[1]:
                    raise Exception(f"Nesting {d} inside of {delimiter} not allowed.")
        new_nodes.append(TextNode(node_parts[1], text_type))

        splitter(TextNode(node_parts[2], TextType.TEXT), delimiter, text_type)

    new_nodes = []
    for text_node in old_nodes:
        if text_node.text_type != TextType.TEXT:
            new_nodes.append(text_node)
        else:
            splitter(text_node, delimiter, text_type)

    return new_nodes
