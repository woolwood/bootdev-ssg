import unittest
from blocks import markdown_to_blocks, block_to_block_type, check_startswith


class TestBlockToBlockType(unittest.TestCase):
    def test_block_to_ordered_list(self):
        input_text = """1. list 
2. of 
3. numbers"""
        expected_result = "ordered_list"
        result = block_to_block_type(input_text)
        self.assertEqual(expected_result, result)

    def test_block_to_quote(self):
        input_text = """>as per my last email
>I'm grinding in the bootmines"""
        expected_result = "quote"
        result = block_to_block_type(input_text)
        self.assertEqual(result, expected_result)

    def test_block_to_unordered_list(self):
        input_text = """* list
- of
* things"""
        expected_result = "unordered_list"
        result = block_to_block_type(input_text)

        self.assertEqual(result, expected_result)

    def test_block_to_code(self):
        input_text = """```
def split_nodes_link(old_nodes):
    

    def splitter(node):
        # Extract all links from node.
        matched_links = extract_markdown_links(node.text)

        # If no link formatting found in node, and node is not empty, pass it as-is to new_nodes.
        if not matched_links:
            if node.text:
                new_nodes.append(node)
            return

        # Split the text node on encountering formatted link in four parts.
        # Everything before link gets TextType.TEXT, everything after is checked again.

        node_parts = re.split(r"(?<!!)\[(.*?)\]\((.*?)\)", node.text, 1)

        # If the first part is empty, do not add it to new_nodes.
        if node_parts[0]:
            new_nodes.append(TextNode(node_parts[0], TextType.TEXT))

        # Construct a TextType.LINK TextNode from 2nd and 3rd part and append to
        # new_nodes and process the remainder.

        new_nodes.append(TextNode(node_parts[1], TextType.LINK, node_parts[2]))
        splitter(TextNode(node_parts[3], TextType.TEXT))

    new_nodes = []
    for textnode in old_nodes:
        if textnode.text_type != TextType.TEXT:
            new_nodes.append(textnode)
        else:
            splitter(textnode)

    return new_nodes
```"""
        expected_result = "code"
        result = block_to_block_type(input_text)
        self.assertEqual(expected_result, result)

    def test_block_to_heading(self):
        input_text = """###### heading ahh text"""
        result = block_to_block_type(input_text)
        expected_result = "heading"

        self.assertEqual(expected_result, result)

    def test_block_to_paragraph(self):
        input_text = """This is a normal paragraph.
It contains nothing fancy :)"""
        result = block_to_block_type(input_text)
        expected_result = "paragraph"

        self.assertEqual(expected_result, result)


class TestMarkDownToBlocks(unittest.TestCase):
    def test_split_document(self):
        input_text = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.








* This is the first list item in a list block
* This is a list item
* This is another list item
"""

        result = markdown_to_blocks(input_text)
        expected_result = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            """* This is the first list item in a list block
* This is a list item
* This is another list item""",
        ]
        self.assertEqual(result, expected_result)

        input_text = " # heading"
        result = markdown_to_blocks(input_text)
        expected_result = ["# heading"]
        self.assertEqual(result, expected_result)
