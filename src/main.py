from textnode import TextNode, TextType
from move_static import *
import sys
import os

basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

src_path = os.path.expanduser(f"{basepath}static")
target_path = os.path.expanduser(f"{basepath}docs")

print(f"Source: {src_path}; Destination: {target_path}")
def main():
    copy_files(src_path, target_path)

    generate_pages_recursive(f"{basepath}content", f"{basepath}template.html", f"{basepath}docs")

main()