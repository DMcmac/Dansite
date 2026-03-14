from textnode import TextNode, TextType
from enum import Enum

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



        

