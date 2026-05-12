from textnode import TextNode
from copystatic import copy_static
from generate import generate_page

def main():
    copy_static()
    generate_page("content/index.md", "template.html", "public/index.html")

main()