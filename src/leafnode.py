from htmlnode import HTMLNode
import re

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props=props)
    
    def to_html(self):
        if self.value is None:
            raise ValueError("A leafnode must have a value")
        
        text = str(self.value)
        text = re.sub(r"\s+", " ", text)
        if not self.tag:
            return text
        return f"<{self.tag}{self.props_to_html()}>{text}</{self.tag}>"
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"