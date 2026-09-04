import unittest
from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType


class TestMarkdownBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_large_empty_blocks(self):
        md = """
This is **bolded** paragraph



This is another paragraph with _italic_ text and `code` here,
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here,\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_heading(self):
        md = "### This is a heading block"
        block_type = block_to_block_type(md)
        self.assertEqual(
            block_type, BlockType.HEADING
            
        )

    def test_almost_heading(self):
        md = "##Almost a heading"
        block_type = block_to_block_type(md)
        self.assertEqual(
            block_type, BlockType.PARAGRAPH
        )

    def test_multiline_block(self):
        md = "```\nThis is a multiline code block```"
        block_type = block_to_block_type(md)
        self.assertEqual(
            block_type, BlockType.CODE
        )

    def test_almost_code(self):
        md = "``\nNot quite a code block```"
        block_type = block_to_block_type(md)
        self.assertEqual(
            block_type, BlockType.PARAGRAPH
        )

    def test_still_not_code(self):
        md = "```\nStill not code``"
        block_type = block_to_block_type(md)
        self.assertEqual(
            block_type, BlockType.PARAGRAPH
        )

    def test_quote_block(self):
        md = ">This is quote block\n> I am testing multiple lines"
        block_type = block_to_block_type(md)
        self.assertEqual(
            block_type, BlockType.QUOTE
        )

    def test_not_quote(self):
        md = ">This is quote block\n I am testing multiple lines"
        block_type = block_to_block_type(md)
        self.assertEqual(
            block_type, BlockType.PARAGRAPH
        )

    def test_unorderd_list(self):
        md = "- This is an unordered list\n- With one line after the other"
        block_type = block_to_block_type(md)
        self.assertEqual(
            block_type, BlockType.UNORDERED_LIST
        )

    def test_not_unorder_list(self):
        md = "- Almost an unordered list\n But not quite"
        block_type = block_to_block_type(md)
        self.assertEqual(
            block_type, BlockType.PARAGRAPH
        )

    def test_ordered_list(self):
        md = "1. This\n2. is\n3. an\n4. ordered\n5. list"
        block_type = block_to_block_type(md)
        self.assertEqual(
            block_type, BlockType.ORDERED_LIST
        )

    def test_almost_ordered(self):
        md = "1. This\n3. is\n4. unordered"
        block_type = block_to_block_type(md)
        self.assertEqual(
            block_type, BlockType.PARAGRAPH
        )

    def test_also_almost_ordered(self):
        md = "1. This\n2.is\n3. close"
        block_type = block_to_block_type(md)
        self.assertEqual(
            block_type, BlockType.PARAGRAPH
        )