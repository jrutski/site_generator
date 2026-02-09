from textnode import TextNode, TextType
from move_static import *

src_path = os.path.expanduser("~/projects/site_generator/static")
target_path = os.path.expanduser("~/projects/site_generator/public")

def main():
    copy_files(src_path, target_path)

    generate_pages_recursive('/home/jrutski/projects/site_generator/content', '/home/jrutski/projects/site_generator/template.html', '/home/jrutski/projects/site_generator/public')

main()