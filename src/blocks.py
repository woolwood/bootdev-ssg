import re
from enum import Enum


# Put the possible block types in an enum to use in case matching.
class BlockType(Enum):
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"
    PARAGRAPH = "paragraph"


def markdown_to_blocks(markdown):
    split_blocks = markdown.split("\n\n")
    return [x.strip() for x in split_blocks if x]


def is_ordered_list(input_list):
    for i, x in enumerate(input_list):
        if not x.startswith(f"{i+1}. "):
            return False
    return True


def block_to_block_type(markdown):
    bullets = ("* ", "- ")
    if re.match("^#{1,6} ", markdown):
        return BlockType.HEADING
    elif markdown.startswith("```") and markdown.endswith("```"):
        return BlockType.CODE
    elif all([x.startswith(">") for x in markdown.split("\n")]):
        return BlockType.QUOTE
    elif all([x.startswith(bullets) for x in markdown.split("\n")]):
        return BlockType.ULIST
    elif is_ordered_list(markdown.split("\n")):
        return BlockType.OLIST
    else:
        return BlockType.PARAGRAPH
