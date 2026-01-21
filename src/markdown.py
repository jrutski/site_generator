import re
from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    ret_nodes = []
    for node in old_nodes:
        new_nodes = []
        if node.text_type != TextType.TEXT:
            ret_nodes.append(node)
            continue
        new_text = node.text.split(delimiter)
        if len(new_text) % 2 == 0:
            raise SyntaxError("Invalid markdown: missing closing delimeter, or none found")
        for i in range(len(new_text)):
            if new_text[i] == "":
                continue
            if i %2 == 0:
                new_nodes.append(TextNode(new_text[i], TextType.TEXT))
            else:
                new_nodes.append(TextNode(new_text[i], text_type))
        ret_nodes.extend(new_nodes)
    return ret_nodes

def extract_markdown_images(text):
    reg_ex = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(reg_ex, text)
    return matches

def extract_markdown_links(text):
    reg_ex = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(reg_ex, text)
    return matches

def split_nodes_image(old_nodes):
    ret_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            ret_nodes.append(node)
            continue
        full_text = node.text
        ext_images = extract_markdown_images(full_text)
        if len(ext_images) == 0:
            ret_nodes.append(node)
            continue
        for image in ext_images:
            split_text = full_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(split_text) != 2:
                raise SyntaxError("Invalid markdown: missing closing delimeter, or none found")
            if split_text[0] != '':
                ret_nodes.append(TextNode(split_text[0], TextType.TEXT))
            ret_nodes.append(TextNode(image[0], TextType.IMAGE, image[1],))
            full_text = split_text[1]
        if full_text != '':
            ret_nodes.append(TextNode(full_text, TextType.TEXT))
    return ret_nodes

def split_nodes_link(old_nodes):
    ret_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            ret_nodes.append(node)
            continue
        full_text = node.text
        ext_links = extract_markdown_links(full_text)
        if len(ext_links) == 0:
            ret_nodes.append(node)
            continue
        for link in ext_links:
            split_text = full_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(split_text) != 2:
                raise SyntaxError("Invalid markdown: missing closing delimeter, or none found")
            if split_text[0] != '':
                ret_nodes.append(TextNode(split_text[0], TextType.TEXT))
            ret_nodes.append(TextNode(link[0], TextType.LINK, link[1],))
            full_text = split_text[1]
        if full_text != '':
            ret_nodes.append(TextNode(full_text, TextType.TEXT))
    return ret_nodes

def text_to_textnodes(text):
    src_nodes = [TextNode(text, TextType.TEXT)]
    src_nodes = split_nodes_delimiter(src_nodes, "**", TextType.BOLD)
    src_nodes = split_nodes_delimiter(src_nodes, "_", TextType.ITALIC)
    src_nodes = split_nodes_delimiter(src_nodes, "`", TextType.CODE)
    src_nodes = split_nodes_image(src_nodes)
    src_nodes = split_nodes_link(src_nodes)
    return src_nodes