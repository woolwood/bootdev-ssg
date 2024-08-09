from textnode import TextNode, text_type_bold
from htmlnode import HTMLNode


def main():
    text_node = TextNode("This is a text node", text_type_bold, "https://www.boot.dev")

    print(text_node)


main()
