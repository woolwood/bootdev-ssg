class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self):

        return (
            f"tag = {self.tag}, value = {self.value}, "
            f"children = {self.children}, props = {self.props}"
        )

    def to_html(self):
        raise NotImplementedError("function to_html not implemented")

    def props_to_html(self):
        if self.props == None:
            return ""
        s = ""
        for k, v in self.props.items():
            s += f' {k}="{v}"'
        return s


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.children == None:
            raiseValueError("ParentNode must have children")
        if self.tag == None:
            raiseValueError("ParentNode must have tags")

        else:

            if len(self.children) == 0:
                return ""
                # return f"<{self.tag}>{children_html}</{self.tag}>"
            else:
                # children_html = ""
                # children_html += self.children[0].to_html()
                self.children = self.children[:-1]
                return self.to_html() + self.children[0].to_html()

            # children_html = ""
            # for child in self.children:
            #     children_html += child.to_html()

            # return f"<{self.tag}>{children_html}</{self.tag}>"

            # list(map(lambda a: a.to_html, self.children))
            # f'<{self.tag}>{self.children.to_html()}</{self.tag}>'


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.children:
            raiseValueError("LeafNode cannot have children")

        if self.value == None:
            raise ValueError("LeafNode.value has no value")
        if self.tag == None:
            return self.value
        else:
            return f"<{self.tag}{self.props_to_html()}>" f"{self.value}</{self.tag}>"
