class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self):
        return (
            f"HTMLNode(tag = {self.tag}, value = {self.value}, "
            f"children = {self.children}, props = {self.props})"
        )

    def __eq__(self, other):
        return (
            self.tag == other.tag
            and self.value == other.value
            and self.children == other.children
            and self.props == other.props
        )

    def to_html(self):
        """This method is overridden in inheriting objects."""
        raise NotImplementedError("function to_html not implemented")

    def props_to_html(self):
        """Take key, value pairs from props dict and convert into HTML."""
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
        """Construct HTML from ParentNode."""

        # Recurse through all child elements in self.children
        if self.children == None:
            raise ValueError("ParentNode must have children")
        if self.tag == None:
            raise ValueError("ParentNode must have tags")

        else:
            children_html = ""
            for child in self.children:
                children_html += child.to_html()

            return f"<{self.tag}>{children_html}</{self.tag}>"

    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        """Construct HTML from LeafNode."""

        if self.children:
            raise ValueError("LeafNode cannot have children")

        if self.value == None:
            raise ValueError("LeafNode.value has no value")
        if self.tag == None:
            return self.value
        else:
            return f"<{self.tag}{self.props_to_html()}>" f"{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
