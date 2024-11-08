import re
import os
import shutil
from pathlib import Path


from markdown_to_html_node import markdown_to_html_node


def extract_title(markdown):
    """Fetch the h1 header from the markdown input"""
    if not re.match(r"^#\s(.+)", markdown):
        raise Exception("Document must have h1 heading.")
    title = re.match(r"^#\s(.+)", markdown).group(1)
    return title


def copy_over_files(src, dst):
    """Copy files to target directory"""
    src_files = os.listdir(src)
    if os.path.exists(dst):
        shutil.rmtree(dst)
        print(f"Destination exists, deleting {dst}")
    os.mkdir(dst)
    print(f"Creating {dst}")

    for filename in src_files:
        filepath = os.path.join(src, filename)
        if os.path.isfile(filepath):
            shutil.copy2(filepath, dst)
            print(f"Copied {filepath} to {dst}")
        if os.path.isdir(filepath):
            dest_filepath = os.path.join(dst, filename)
            print(f"{filepath} is directory, creating {dest_filepath}")
            copy_over_files(filepath, dest_filepath)


def generate_page(from_path, dest_path, template_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path) as sourcefile:
        sourcefile_content = sourcefile.read()

    with open(template_path) as template:
        template_content = template.read()

    content_html = markdown_to_html_node(sourcefile_content).to_html()
    # print(content_html)

    page_title = extract_title(sourcefile_content)

    page_html = template_content.replace("{{ Title }}", page_title).replace(
        "{{ Content }}", content_html
    )

    dir_path = os.path.dirname(dest_path)
    # print(dest_path)

    os.makedirs(dir_path, exist_ok=True)

    with open(dest_path, "w") as dest_file:
        dest_file.write(page_html)


def generate_pages_recursive(dir_path_content, dest_dir_path, template_path):
    current_path_contents = os.listdir(dir_path_content)
    print(current_path_contents)
    for filename in current_path_contents:
        filepath = Path(dir_path_content, filename)
        if os.path.isdir(filepath):
            dest_filepath = Path(dest_dir_path, filename)
            print(dest_filepath)
            generate_pages_recursive(filepath, dest_filepath, template_path)
        if os.path.isfile(filepath):
            if filepath.suffix == ".md":
                dest_filepath = Path(dest_dir_path, filename).with_suffix(".html")
                generate_page(filepath, dest_filepath, template_path)
