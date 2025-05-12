from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def ___init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("No value provided for HTML")
        
        if self.tag is None:
            return str(self.value)
        
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"{self.__class__.__name__}({self.tag}, {self.value}, {self.props})"
