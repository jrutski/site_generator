class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("not yet implented")
    
    def props_to_html(self):
        if self.props is None:
            return ""
        ret_str = ""
        for key, value in self.props.items():
            ret_str += f" {key}=\"{value}\""
        return ret_str
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("HTML parents require tags")
        if self.children is None:
            raise ValueError("Child cannot be None")
        leaf_str = ""
        for leaf in self.children:
            leaf_str += leaf.to_html()
        return f"<{self.tag}{self.props_to_html()}>{leaf_str}</{self.tag}>"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("all html leaves must have a value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.props})"