def markdown_to_blocks(markdown):
    block_list = []
    blocks = markdown.split("\n\n")
    for b in blocks:
        stripped_block = b.strip()
        if stripped_block == "":
            continue
        block_list.append(stripped_block)
    return block_list    