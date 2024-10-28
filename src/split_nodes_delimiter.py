from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """
    Takes a list of 'old nodes', delimiter and text type,
    returns new list of nodes split by text type.
    """

    def splitter(node, delimiter, text_type):
        # If delimiter not found in text, pass it as-is to new_nodes.
        if delimiter not in node.text:
            if node.text:
                new_nodes.append(node)
            return
        # If delimiter number is odd, there is an improperly closed tag.
        if node.text.count(delimiter) % 2 != 0:
            raise Exception(
                f"Invalid markdown code, closing delimiter {delimiter} not found."
            )

        delimiters = ["*", "**"]

        # Split the text node on the delimiter in three parts, the last part is
        # the remainder and will be checked later
        node_parts = node.text.split(delimiter, 2)

        # If the first part is empty, do not add it to new_nodes.
        if node_parts[0]:
            new_nodes.append(TextNode(node_parts[0], TextType.TEXT))

        # Consecutive delimiters result in empty fields. Don't allow for it.
        if node_parts[1] == "":
            raise Exception(
                f"Empty field. Consecutive delimiter {delimiter} not allowed."
            )

        # Do not allow nested delimiters, except inside of CODE TextTypes.
        if text_type != TextType.CODE:
            for d in delimiters:
                if d in node_parts[1]:
                    raise Exception(f"Nesting {d} inside of {delimiter} not allowed.")

        # Append the processed node after these checks and process the remainder.
        new_nodes.append(TextNode(node_parts[1], text_type))

        splitter(TextNode(node_parts[2], TextType.TEXT), delimiter, text_type)

    new_nodes = []
    for text_node in old_nodes:
        if text_node.text_type != TextType.TEXT:
            new_nodes.append(text_node)
        else:
            splitter(text_node, delimiter, text_type)

    return new_nodes
