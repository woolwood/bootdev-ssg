import re


def extract_markdown_images(text):
    """
    Identify image formatting in a markdown text and form a list of tuples (alt text, image uri).
    """
    return re.findall(r"\!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text):
    """
    Identify link formatting in a markdown text and form a list of tuples (anchor text, link uri).
    """
    return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)
