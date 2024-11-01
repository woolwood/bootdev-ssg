import re


def markdown_to_blocks(markdown):
    split_blocks = markdown.split("\n\n")
    return [x.strip() for x in split_blocks if x]


def is_ordered_list(input_list):
    for i, x in enumerate(input_list):
        if not x.startswith(f"{i+1}. "):
            return False
    return True


def check_startswith(input_text):
    if input_text.startswith("h"):
        return "Yeah"


def block_to_block_type(markdown):
    bullets = ("*", "-")
    if re.match("#{1,6} ", markdown):
        return "heading"
    # if markdown.startswith("# "):
    #     return "heading"
    elif markdown.startswith("```") and markdown.endswith("```"):
        return "code"
    elif all([x.startswith(">") for x in markdown.split("\n")]):
        return "quote"
    elif all([x.startswith(bullets) for x in markdown.split("\n")]):
        return "unordered_list"
    elif is_ordered_list(markdown.split("\n")):
        return "ordered_list"
    else:
        return "paragraph"
