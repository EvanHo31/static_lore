from textnode import TextNode, TextType
from leafnode import LeafNode
from parentnode import ParentNode
from extraction import split_nodes_image, split_nodes_link, split_nodes_delimiter
from blocks import block_to_block_type, BlockType
import re

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
    # if text == "":
    #     return []
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

def clean_white_spaces(text:str):
    # text = text.strip()
    text = re.sub(r"\s+", " ", text)
    return text

def paragrpah_to_html_node(block:str):
    textnodes = text_to_text_nodes(block)
    html_nodes = []
    for node in textnodes:
        node.text = clean_white_spaces(node.text)
        html_nodes.append(text_node_to_html_node(node))
    paragraph = ParentNode("p", html_nodes)
    return paragraph

def code_to_html_node(block:str):
    textnode = TextNode(block[4:-3], TextType.CODE)
    return ParentNode("pre", [text_node_to_html_node(textnode)])

def header_to_html_node(block:str):
    size = 1
    while block[size] != " ": size+=1
    textnodes = text_to_text_nodes(block[size+1:])
    html_nodes = []
    for node in textnodes:
        # node.text = clean_white_spaces(node.text)
        html_nodes.append(text_node_to_html_node(node))
    header = ParentNode(f"h{size}", html_nodes)
    return header

def quote_to_html_node(block:str):
    html_nodes = []
    lines = block.split("\n")
    for line in lines:
        line = re.findall(r"^>\s?(.*)", line)[0]
        text_nodes = text_to_text_nodes(line)
        nodes = []
        for node in text_nodes:
            nodes.append(text_node_to_html_node(node))
        html_nodes.extend(nodes)
    quote = ParentNode("blockquote", html_nodes)
    return  quote

def ulist_to_html_node(block:str):
    list_item = []
    lines = block.split("\n")
    for line in lines:
        line = line[2:]
        text_nodes = text_to_text_nodes(line)
        nodes = []
        for node in text_nodes:
            nodes.append(text_node_to_html_node(node))
        list_item.append(ParentNode("li", nodes))
    return ParentNode("ul", list_item)

def olist_to_html_node(block:str):
    list_item = []
    lines = block.split("\n")
    for line in lines:
        line = line[3:]
        text_nodes = text_to_text_nodes(line)
        nodes = []
        for node in text_nodes:
            nodes.append(text_node_to_html_node(node))
        list_item.append(ParentNode("li", nodes))
    return ParentNode("ol", list_item)

def markdown_to_html_node(markdown:str):
    blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.PARAGRAPH:
                html_nodes.append(paragrpah_to_html_node(block))

            case BlockType.CODE:
                html_nodes.append(code_to_html_node(block))
            
            case BlockType.HEADING:
                html_nodes.append(header_to_html_node(block))
            
            case BlockType.QUOTE:
                html_nodes.append(quote_to_html_node(block))

            case BlockType.UNORDERED_LIST:
                html_nodes.append(ulist_to_html_node(block))

            case BlockType.ORDERED_LIST:
                html_nodes.append(olist_to_html_node(block))

            case _:
                raise ValueError("invalid block type")
            
    div = ParentNode("div", html_nodes)
    return div
