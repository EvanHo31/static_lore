from textnode import TextNode, TextType
from leafnode import LeafNode

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
