from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes:list, delimiter:str, text_type:TextType):
    if not delimiter:
        raise ValueError("cannot split with empty delimiter")
    new_nodes = []
    for node in old_nodes:
        node:TextNode
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue
        splited = node.text.split(delimiter)
        # delimiter not found
        if len(splited) == 1:
            new_nodes.append(node)
            continue
        # missing closing delimiter
        if len(splited)%2 == 0:
            raise ValueError(f"invalid markdown, closing delimiter {delimiter} not found")
        is_block = False
        for part in splited:
            if part == "":
                pass
            elif not is_block:
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                new_nodes.append(TextNode(part, text_type))
            is_block = not is_block
    return new_nodes

def extract_markdown_links(text:str):
    matches = re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)
    return matches

def extract_markdown_images(text:str):
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        node:TextNode
        if node.text_type is TextType.CODE:
            new_nodes.append(node)
            continue
        images = extract_markdown_images(node.text)
        if len(images) == 0:
            new_nodes.append(node)
            continue
        i = 0; j = 0; 
        for image in images:
            j = str(node.text).find(image[0])
            temp_list = [TextNode(node.text[i:j-2], TextType.TEXT), TextNode(image[0], TextType.IMAGE, image[1])]
            new_nodes.extend(temp_list)
            i = j + len(image[0]) + len(image[1]) + 3
        if len(node.text) != i:
            new_nodes.append(TextNode(node.text[i:], TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        node:TextNode
        if node.text_type is TextType.CODE:
            new_nodes.append(node)
            continue
        links = extract_markdown_links(node.text)
        if len(links) == 0:
            new_nodes.append(node)
            continue
        i = 0; j = 0; 
        for link in links:
            j = str(node.text).find(link[0])
            temp_list = [TextNode(node.text[i:j-1], TextType.TEXT), TextNode(link[0], TextType.LINK, link[1])]
            new_nodes.extend(temp_list)
            i = j + len(link[0]) + len(link[1]) + 3
        if len(node.text) != i:
            new_nodes.append(TextNode(node.text[i:], TextType.TEXT))
    return new_nodes
            
def extract_title(markdown:str):
    lines = markdown.split("\n")
    title = ""
    for line in lines:
        if line.startswith("# "):
            title = line[2:]
    if not title:
        raise Exception("Title (h1)  not found in markdown file") 
    return title