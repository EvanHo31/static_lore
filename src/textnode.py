from enum import Enum

class TextType(Enum):
    TEXT = 1
    BOLD = 2
    ITALIC = 3
    CODE = 4
    LINK = 5
    IMAGE = 6

class TextNode():
    def __init__(self, text, text_type, url=None):
        super().__init__()
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, other):
        if type(self) != type(other):
            raise TypeError(f"Connot compare between {type(self)} and {type(other)}")
        if self.text != other.text:
            return False
        if self.text_type != other.text_type:
            return False
        if self.url != other.url:
            return False
        return True
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
    