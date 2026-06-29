from textnode import TextNode, TextType
from enum import Enum
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        split_node_list = node.text.split(delimiter)
        if len(split_node_list) % 2 == 0:
            raise Exception("missing delimiter")
        for n in range(len(split_node_list)):
            if split_node_list[n] != "":
                if n % 2 == 0:
                    string_node = TextNode(split_node_list[n], TextType.TEXT)
                    new_nodes.append(string_node)
                else:
                    newer_node = TextNode(split_node_list[n], text_type)
                    new_nodes.append(newer_node)
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        image_tuples = extract_markdown_images(node.text)
        if image_tuples == []:
            new_nodes.append(node)
            continue
        remaining_text = node.text
        for t in image_tuples:
            text_nodes = remaining_text.split(f"![{t[0]}]({t[1]})", 1)
            if text_nodes[0] != "":
                new_text_node = TextNode(text_nodes[0], TextType.TEXT)
                new_nodes.append(new_text_node)
            image_node = TextNode(t[0], TextType.IMAGE, t[1])
            new_nodes.append(image_node)
            remaining_text = text_nodes[1]
        if remaining_text != "":
            closing_node = TextNode(remaining_text,TextType.TEXT)
            new_nodes.append(closing_node)

    return new_nodes

    
def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        link_tuples = extract_markdown_links(node.text)
        if link_tuples == []:
            new_nodes.append(node)
            continue
        remaining_text = node.text
        for t in link_tuples:
            text_nodes = remaining_text.split(f"[{t[0]}]({t[1]})", 1)
            if text_nodes[0] != "":
                new_text_node = TextNode(text_nodes[0], TextType.TEXT)
                new_nodes.append(new_text_node)
            link_node = TextNode(t[0], TextType.HYPERLINK, t[1])
            new_nodes.append(link_node)
            remaining_text = text_nodes[1]
        if remaining_text != "":
            closing_node = TextNode(remaining_text,TextType.TEXT)
            new_nodes.append(closing_node)

    return new_nodes

def text_to_textnodes(text):
    starting_text = [TextNode(text, TextType.TEXT)]
    bold_split = split_nodes_delimiter(starting_text, "**", TextType.BOLD)
    code_split = split_nodes_delimiter(bold_split, "`", TextType.CODE)
    italic_split = split_nodes_delimiter(code_split, "_", TextType.ITALIC)
    image_split = split_nodes_image(italic_split)
    link_split = split_nodes_link(image_split)
    return link_split

        

