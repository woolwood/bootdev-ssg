from generate_pages import copy_over_files, generate_page, generate_pages_recursive


def main():

    copy_over_files("static", "public")
    generate_pages_recursive("content", "public", "template.html")
    # generate_page("content/index.md", "public/index.html", "template.html")


main()
