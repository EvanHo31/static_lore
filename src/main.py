from textnode import TextNode
from copystatic import copy_static
from generate import generate_pages_recursive

def main():
    copy_static()
    generate_pages_recursive("content", "template.html", "public")

main()
exit()