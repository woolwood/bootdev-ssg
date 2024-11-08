import re

def extract_title(markdown):
    if not re.match(r"^#\s(.+)", markdown):
        raise Exception("Document must have h1 heading.")
    title = re.match(r"^#\s(.+)", markdown).group(1)
    return title
