from htmlnode import HTMLNode, ParentNode
from leafnode import LeafNode
from enum import Enum

import re

class BlockType(Enum):
    PARAGRAPH     = "paragraph"
    HEADING       = "heading"
    CODE          = "code"
    QUOTE         = "quote"
    UNORDEREDLIST = "unordered_list"
    ORDEREDLIST   = "ordered_list"

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

def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(
                TextNode(
                    image[0],
                    TextType.IMAGE,
                    image[1],
                )
            )
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text_in=text, type_in=TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def markdown_to_blocks(markdown):
    block_strings = markdown.split("\n\n")
    cleaned_blocks = list(map(lambda x: [x.strip() for x in block_strings if x], block_strings))

    return cleaned_blocks[0]

def block_to_block_type(md_block):
    if len(md_block) == 0:
        return BlockType.PARAGRAPH

    delimiter = md_block.split()[0].strip()

    match delimiter:
        case "#" | "##" | "###" | "####" | "#####" | "######":
            return BlockType.HEADING
        case "```":
            return BlockType.CODE
        case ">":
            return BlockType.QUOTE
        case "-":
            return BlockType.UNORDEREDLIST
        case str() if re.fullmatch(r"\d*.", delimiter):
            return BlockType.ORDEREDLIST
        case _:
            return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    md_blocks = markdown_to_blocks(markdown)
    children = []

    for block in md_blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    match block_type:
        case BlockType.CODE:
            if block.startswith("```") and block.endswith("```"):
                value = block[4:-3]
                text_node = TextNode(value, TextType.TEXT)
                child = text_node_to_html_node(text_node)
                code = ParentNode("code", [child])
                return ParentNode("pre", [code])
            else:
                raise ValueError("Invalid code block")
        case BlockType.HEADING:
            depth = 0
            for char in block:
                if char == "#":
                    depth += 1
                else:
                    break
            if depth + 1 >= len(block):
                raise ValueError(f"Invalid heading depth: {depth}")
            text = block[depth+1:]
            children = text_to_children(text)
            return ParentNode(f"h{depth}", children)

        case BlockType.ORDEREDLIST:
            items = block.split("\n")
            html_items = []
            for item in items:
                text = item[3:]
                children = text_to_children(text)
                html_items.append(ParentNode("li", children))
            return ParentNode("ol", html_items)

        case BlockType.UNORDEREDLIST:
            items = block.split("\n")
            html_items = []
            for item in items:
                text = item[2:]
                children = text_to_children(text)
                html_items.append(ParentNode("li", children))
            return ParentNode("ul", html_items)

        case BlockType.PARAGRAPH:
            lines = block.split("\n")
            paragraph = ' '.join(lines)
            children = text_to_children(paragraph)
            return ParentNode("p", children)

        case BlockType.QUOTE:
            lines = block.split("\n")
            new_lines = []
            for line in lines:
                if line.startswith(">"):
                    new_lines.append(line.lstrip(">").strip())
                else:
                    raise ValueError("Invalid quote block")
            content = " ".join(new_lines)
            children = text_to_children(content)
            return ParentNode("blockquote", children)

        case _:
            raise ValueError(f"Invalide BlockType: {block_type}")

def text_to_children(text):
    nodes = text_to_textnodes(text)
    children = []
    for node in nodes:
        html_node = text_node_to_html_node(node)
        children.append(html_node)
    return children