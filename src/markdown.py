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