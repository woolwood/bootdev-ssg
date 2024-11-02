from blocks import BlockType, markdown_to_blocks, block_to_block_type
from htmlnode import HTMLNode, ParentNode, LeafNode
from textnode_to_html_node import textnode_to_html_node
from text_to_textnode import text_to_textnodes
import re


def strip_blocklevel_md(block_type, block):
    """
    Strip out block level markdown, returning a list of strings.
    """
    match block_type:
        case BlockType.QUOTE:
            return [x.lstrip(">").lstrip() for x in block.split("\n")]

        case BlockType.ULIST:
            return [x.lstrip("*- ").lstrip() for x in block.split("\n")]

        case BlockType.OLIST:
            return [re.sub(r"^(\d+)\. *", "", x).lstrip() for x in block.split("\n")]

        case BlockType.CODE:
            return [block[3:-3]]

        case BlockType.HEADING:
            # Headings can't be multi-line, no need to split.
            return [block.lstrip("# ")]

        case BlockType.PARAGRAPH:
            return [x for x in block.split("\n")]


def text_to_children(text):
    """
    Processes a text string to return a list of leafnodes.
    """
    textnodes = text_to_textnodes(text)
    leafnodes = []
    for node in textnodes:
        leafnodes.append(textnode_to_html_node(node))
    return leafnodes


def process_inline_md(stripped_block):
    """
    Process inline markdown to return a list of leafnodes.
    """
    processed_block = []
    for line in stripped_block:
        processed_block.extend(text_to_children(line))
    return processed_block


def process_wrap_inline_md(tag, stripped_block):
    """
    Wraps LeafNodes processed from a stripped block in a list of ParentNodes with necessary tag.
    """
    wrapped_nodes = []
    for line in stripped_block:
        children = []
        children.extend(text_to_children(line))
        wrapped_nodes.append(ParentNode(tag, children))
    return wrapped_nodes


def bypass_inline_processing(stripped_block):
    """
    Return a LeafNode from a single text input with no inline processing.
    """
    return LeafNode(None, stripped_block[0])


def block_to_htmlnode(block):
    """
    Processes a markdown block into a ParentNode type HTMLNode.
    """
    # Identify the type of block
    block_type = block_to_block_type(block)

    # Strip the block level markdown, process the inline markdown and
    # wrap inside a HTMLNode
    stripped_block = strip_blocklevel_md(block_type, block)
    match block_type:
        case BlockType.QUOTE:
            processed_block = process_inline_md(stripped_block)
            return ParentNode("blockquote", processed_block)

        case BlockType.ULIST:
            wrapped_nodes = process_wrap_inline_md("li", stripped_block)
            return ParentNode("ul", wrapped_nodes)

        case BlockType.OLIST:
            wrapped_nodes = process_wrap_inline_md("li", stripped_block)
            return ParentNode("ol", wrapped_nodes)

        case BlockType.CODE:
            # <code> block must be nested inside a <pre>
            # Do not process text inside a code block

            leaf_node = bypass_inline_processing(stripped_block)
            code_node = ParentNode("code", [leaf_node])
            return ParentNode("pre", [code_node])

        case BlockType.HEADING:
            pound_count = len(re.match("^(#+)", block).group(0))
            processed_block = process_inline_md(stripped_block)
            return ParentNode(f"h{pound_count}", processed_block)

        case BlockType.PARAGRAPH:
            processed_block = process_inline_md(stripped_block)
            return ParentNode("p", processed_block)


def markdown_to_html_node(markdown):
    """
    Converts a whole markdown input to a HTMLNode.
    """
    block_nodes = []

    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_node = block_to_htmlnode(block)
        block_nodes.append(block_node)

    document_node = HTMLNode("div", children=block_nodes)

    return document_node
