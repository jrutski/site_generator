import os, shutil
from markdown_blocks import markdown_to_html_node


def prep_directory(dir_path):
    print(f"Prep directory: {dir_path}")
    if os.path.exists(dir_path):
        for dir_obj in os.listdir(dir_path):
            if os.path.isdir(os.path.join(dir_path, dir_obj)):
                del_directory(os.path.join(dir_path, dir_obj))
            else:
                os.remove(os.path.join(dir_path, dir_obj))
    else:
        raise FileNotFoundError("Target directory doesn't exist")
    
def del_directory(dir_path):
    for dir_obj in os.listdir(dir_path):
        if os.path.isdir(os.path.join(dir_path, dir_obj)):
            del_directory(os.path.join(dir_path, dir_obj))
        else:
            os.remove(os.path.join(dir_path, dir_obj))
    os.rmdir(dir_path)

def copy_files(src_path, target_path):
    print(f"Copy, Src: {src_path}, Dest: {target_path}")
    prep_directory(target_path)
    if os.path.exists(src_path):
        for dir_obj in os.listdir(src_path):
            if os.path.isfile(os.path.join(src_path, dir_obj)):
                shutil.copy(os.path.join(src_path, dir_obj), os.path.join(target_path, dir_obj))
            else:
                copy_directory(os.path.join(src_path, dir_obj), os.path.join(target_path, dir_obj))
    else:
        raise FileNotFoundError("Source directory doesn't exist")
    
def copy_directory(src_path, target_path):
    os.mkdir(target_path)
    for dir_obj in os.listdir(src_path):
        if os.path.isfile(os.path.join(src_path, dir_obj)):
            shutil.copy(os.path.join(src_path, dir_obj), os.path.join(target_path, dir_obj))
        else:
            copy_directory(os.path.join(src_path, dir_obj), os.path.join(target_path, dir_obj))

def extract_title(markdown):
    if markdown.startswith("# "):
        return markdown[2:]
    else:
        raise Exception("Markdown doesn't include a header")
    
def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, 'r') as f:
        md_contents = f.read()

    with open(template_path, 'r') as f:
        template_contents = f.read()

    html_title = ""
    for line in md_contents.splitlines():
        if line.startswith("# "):
            html_title = extract_title(line)
            break


    md_html_nodes = markdown_to_html_node(md_contents)
    html_string = md_html_nodes.to_html()
    
    final_html = (template_contents.replace('{{ Title }}', html_title).replace('{{ Content }}', html_string))
    final_html = final_html.replace('href="/', f'href="{basepath}')
    final_html = final_html.replace('src="/', f'src="{basepath}')

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, 'w', encoding='utf-8') as f:
        f.write(final_html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    print(f"Recursing: {dir_path_content}")
    for dir_obj in os.listdir(dir_path_content):
        if os.path.isfile(os.path.join(dir_path_content, dir_obj)):
            if dir_obj.endswith('.md'):
                new_filename = dir_obj.removesuffix('.md') + '.html'
                generate_page(os.path.join(dir_path_content, dir_obj), template_path, os.path.join(dest_dir_path, new_filename), basepath)
            else:
                print(f"{dir_obj} is not Markdown. Moving on.")
        else:
            generate_pages_recursive(os.path.join(dir_path_content, dir_obj), template_path, os.path.join(dest_dir_path, dir_obj), basepath)