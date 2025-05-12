from enum import Enum

class TextType(Enum):
    TEXT = 'text'
    BOLD   = 'bold'
    ITALIC = 'italic'
    CODE   = 'code'
    LINK   = 'link'
    IMAGE  = 'image' 

class TextNode():
    def __init__(self, text_in, type_in, url_in=None):
        self.text = text_in
        self.type = type_in
        self.url = url_in

    def __eq__(self, other):
        return self.text == other.text and self.type == other.type and self.url == other.url
    
    def __repr__(self):
        return f'{self.__class__.__name__}({self.text}, {self.type.value}, {self.url})'