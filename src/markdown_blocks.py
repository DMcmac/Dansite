from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    block_list = []
    blocks = markdown.split("\n\n")
    for b in blocks:
        stripped_block = b.strip()
        if stripped_block == "":
            continue
        block_list.append(stripped_block)
    return block_list    

def block_to_block_type(block):
    lines = block.split('\n')
    for i in range(1, 7):
        prefix = '#'
        if block.startswith(prefix * i + ' '):
            return BlockType.HEADING
    if block.startswith('```\n') and block.endswith('```'):
        return BlockType.CODE
    if block.startswith('>'):
        for l in lines:
            if not l.startswith('>'):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith('- '):
        for l in lines:
            if not l.startswith('- '):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    list_order = 1
    if block.startswith(f'{list_order}. '):
        for l in lines:
            if not l.startswith(f'{list_order}. '):
                return BlockType.PARAGRAPH
            elif l.startswith(f'{list_order}. '):
                list_order += 1
        return BlockType.ORDERED_LIST   
        
    return BlockType.PARAGRAPH