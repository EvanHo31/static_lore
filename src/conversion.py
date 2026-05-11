from textnode import TextNode, TextType
from leafnode import LeafNode
from extraction import split_nodes_image, split_nodes_link, split_nodes_delimiter

def text_node_to_html_node(text_node:TextNode):
    tag = ""
    value = text_node.text
    props = {}
    match text_node.text_type:
        case TextType.TEXT:
            tag = None
        case TextType.BOLD:
            tag = "b"
        case TextType.ITALIC:
            tag = "i"
        case TextType.CODE:
            tag = "code"
        case TextType.LINK:
            tag = "a"
            props["href"] = text_node.url
        case TextType.IMAGE:
            tag = "img"
            props["src"] = text_node.url
            props["alt"] = text_node.text
            value = ""
        case _:
            raise TypeError(f"Invalid TextType enum, got{text_node.text_type}")
    leafnode = LeafNode(tag, value, props)
    return leafnode

def text_to_text_nodes(text:str):
    if text == "":
        return []
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_image(nodes)
    return nodes

def markdown_to_blocks(text:str):
    lines = text.split("\n")
    blocks = []
    block = ""
    for line in lines:
        line = line.strip()
        if line == "":
            if block == "":
                continue
            blocks.append(block[:-1])
            block = ""
        else:
            block += line + "\n"
    return blocks