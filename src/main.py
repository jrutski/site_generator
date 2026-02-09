from textnode import TextNode, TextType
from move_static import *
import sys
import os

basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

src_path = os.path.expanduser("./static")
target_path = os.path.expanduser("./docs")

print(f"Source: {src_path}; Destination: {target_path}")
def main():
    copy_files(src_path, target_path)

    generate_pages_recursive("./content", "./template.html", "./docs", basepath)

main()