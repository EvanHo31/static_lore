from conversion import markdown_to_html_node
from extraction import extract_title
from parentnode import ParentNode
import os

def pretty_html_node(node:ParentNode, level=0):
    if type(node) is not ParentNode:
        raise ValueError(f"Expected ParentNode got {type(node)}")
    if level == 0:
        print(f"<ParentNode {node.tag}> {len(node.children)} children")
    for child in node.children:
        if type(child) is ParentNode:
            print(f"{' '*level}+ ParentNode <{child.tag}>")
            pretty_html_node(child, level+1)
        else:
            print(f"{' '*level}| LeafNode <{child.tag}> \"{child.value}\" ({child.props})")
        


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown = ""
    with open(from_path, "r") as f:
        markdown = f.read()
        f.close()
    template = ""
    with open(template_path, "r") as f:
        template = f.read()
        f.close()
    html_node = markdown_to_html_node(markdown)
    pretty_html_node(html_node)
    html_content = html_node.to_html()
    title = extract_title(markdown)
    template = template.replace(r"{{ Title }}", title)
    template = template.replace(r"{{ Content }}", html_content)
    full_path:str = os.path.abspath(dest_path)
    targt_dir = os.path.dirname(full_path)
    if not os.path.exists(targt_dir): 
        os.makedirs(targt_dir)
    with open(dest_path, "w") as f:
        f.write(template)