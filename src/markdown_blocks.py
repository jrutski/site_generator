from enum import Enum
from htmlnode import ParentNode
from markdown import text_to_textnodes
from textnode import text_node_to_html_node, TextNode, TextType


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    ret_blocks = []
    for line in markdown.split("\n\n"):
        if line == '':
            continue
        ret_blocks.append(line.strip('\n'))
    return ret_blocks

def block_to_block_type(block):
    lines = block.split('\n')

    if len(lines) > 1 and lines[0].startswith('```') and lines[-1].startswith('```'):
        return BlockType.CODE
    if block.startswith('> '):
        for line in lines:
            if not line.startswith('> '):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith('- '):
        for line in lines:
            if not line.startswith('- '):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    if block.startswith('1. '):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST
    if block.startswith(('#', '##', '###', '####', '#####', '######')):
        return BlockType.HEADING
    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    md_blocks = markdown_to_blocks(markdown)
    child_nodes = []
    for block in md_blocks:
        html_node = block_to_html_node(block)
        child_nodes.append(html_node)
    return ParentNode("div", child_nodes, None)

def block_to_html_node(block):
    b_type = block_to_block_type(block)
    if b_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if b_type == BlockType.CODE:
        return code_to_html_node(block)
    if b_type == BlockType.UNORDERED_LIST:
        return unordered_list_to_html_node(block)
    raise ValueError("Invalid block type")

def text_to_child(text):
    nodes = text_to_textnodes(text)
    child_nodes = []
    for node in nodes:
        html_node = text_node_to_html_node(node)
        child_nodes.append(html_node)
    return child_nodes

def paragraph_to_html_node(block):
    lines = block.split("\n")
    text = " ".join(lines)
    children = text_to_child(text)
    return ParentNode('p', children)

def heading_to_html_node(block):
    pass

def code_to_html_node(block):
    raw_text = TextNode(block[4:-3], TextType.TEXT)
    child_node = text_node_to_html_node(raw_text)
    return ParentNode("pre", ParentNode("code", child_node))

def ordered_list_to_html_node(block):
    list_items = block.split('\n')
    html_list = []
    for item in list_items:
        line = item.split('. ', 1)
        list_text = line[1]
        child = text_to_child(list_text)
        html_list.append(ParentNode('li', child))
    return ParentNode('ol', html_list)

def unordered_list_to_html_node(block):
    list_items = block.split('\n')
    html_list = []
    for item in list_items:
        line = item[2:]
        child = text_to_child(line)
        html_list.append(ParentNode('li', child))
    return ParentNode('ul', html_list)


def quote_to_html_node(block):
    pass
