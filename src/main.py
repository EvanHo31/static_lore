from copystatic import copy_static
from generate import generate_pages_recursive
import sys

def main():
    if len(sys.argv) >= 2:
        basepath = sys.argv[1]
    else:
        basepath = "/"
    print(f"buildinf pages at {basepath}")
    copy_static("docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)

main()