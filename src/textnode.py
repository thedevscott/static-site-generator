from leafnode import LeafNode
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

def text_node_to_html_node(text_node):
    if text_node.type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    if text_node.type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    if text_node.type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    if text_node.type == TextType.CODE:
        return LeafNode("code", text_node.text)
    if text_node.type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    if text_node.type == TextType.IMAGE:
        return LeafNode(tag="img", value="", props={"src": text_node.url, "alt": text_node.text})
    raise ValueError(f"invalid text type: {text_node.type}")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        
        if old_node.type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        split_nodes = []
        sections = old_node.text.split(delimiter)
        
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown. unclosed format.")

        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(text_in=sections[i], type_in=TextType.TEXT))
            else:
                split_nodes.append(TextNode(text_in=sections[i], type_in=text_type))
        
        new_nodes.extend(split_nodes)
    
    return new_nodes

