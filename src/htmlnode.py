
class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        html_output = ""
        if self.props is None:
            return html_output
        for k in self.props:
            html_output += f' {k}="{self.props[k]}"'
        return html_output
    
    def __repr__(self):
        return (f"Tag = {self.tag}, Value = {self.value}, Children = {self.children}, Props = {self.props}")


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value,None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("Missing value")
        if not self.tag:
            return self.value
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
    
    def __repr__(self):
        return (f"Tag = {self.tag}, Value = {self.value}, Props = {self.props}")
    

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("No tag")
        if self.children is None:
            raise ValueError("Missing child value")
        inner_string = ""
        for child in self.children:
            inner_string += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{inner_string}</{self.tag}>"
