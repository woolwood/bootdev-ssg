class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self):
        
        return (f'tag = {self.tag}, value = {self.value}, '
        f'children = {self.children}, props = {self.props}')

    def to_html(self):
        raise NotImplementedError("function to_html not implemented")

    def props_to_html(self):
        if self.props == None:
            return ""
        s = ""
        for k, v in self.props.items():
            s += (f' {k}="{v}"')
        return s

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.children:
            raiseValueError("LeafNode cannot have children")

        if self.value == None:
            raise ValueError("LeafNode.value has no value")
        if self.tag == None:
            return value
        else:
            return (f"<{self.tag}{self.props_to_html()}>"
            f"{self.value}</{self.tag}>")