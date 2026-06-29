import unittest
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes
from textnode import TextNode, TextType

class TestInlineMarkdown(unittest.TestCase):
    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold(self):
        node = TextNode("This is text with a **bold block** of text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bold block", TextType.BOLD),
                TextNode(" of text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_miss_delim(self):
        node = TextNode("This is to test a block with a **missing delimiter", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is a text with a [link](www.google.com)"
        )
        self.assertListEqual([("link", "www.google.com")], matches)

    def test_extract_markdown_image_with_link(self):
        matches = extract_markdown_images(
            "This is a text with both a [link](www.google.com) and an ![image](https://image.com/example.png)"
        )
        self.assertListEqual([("image","https://image.com/example.png" )], matches)

    def test_extract_markdown_link_with_image(self):
        matches = extract_markdown_links(
            "This is a text with both a [link](www.google.com) and an ![image](https://image.com/example.png)"
        )
        self.assertListEqual([("link", "www.google.com" )], matches)

    def test_extract_markdown_images_multiple(self):
        matches = extract_markdown_images(
            "This is text with more than one ![image](https://example.png) ![next](https://another.png)"
        )
        self.assertListEqual([("image", "https://example.png"),("next", "https://another.png")], matches)


    def test_split_images(self):
        node = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode(
                "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
            ),
            ],
            new_nodes,
        )


    def test_split_links(self):
        node = TextNode(
        "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("link", TextType.HYPERLINK, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode(
                "second link", TextType.HYPERLINK, "https://i.imgur.com/3elNhQu.png"
            ),
            ],
            new_nodes,
        )

    def test_no_image(self):
        node = TextNode("This a line of text without images or links", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([TextNode("This a line of text without images or links", TextType.TEXT)], new_nodes)

    def test_no_link(self):
        node = TextNode("This a line of text without images or links", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([TextNode("This a line of text without images or links", TextType.TEXT)], new_nodes)


    def test_no_text_between_image(self):
        node = TextNode("This is to test for no text between ![image](https://i.imgur.com/zjjcJKZ.png)![second image](https://i.imgur.com/3elNhQu.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([TextNode("This is to test for no text between ", TextType.TEXT),
                              TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                              TextNode("second image", TextType.IMAGE,"https://i.imgur.com/3elNhQu.png" )],
                              new_nodes)


    def test_no_text_between_link(self):
        node = TextNode("This is to test for no text between [link](https://i.imgur.com/zjjcJKZ.png)[second link](https://i.imgur.com/3elNhQu.png)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([TextNode("This is to test for no text between ", TextType.TEXT),
                              TextNode("link", TextType.HYPERLINK, "https://i.imgur.com/zjjcJKZ.png"),
                              TextNode("second link", TextType.HYPERLINK,"https://i.imgur.com/3elNhQu.png" )],
                              new_nodes)
        
    def test_no_text_before_image(self):
        node = TextNode("![image](https://i.imgur.com/zjjcJKZ.png) with no text before", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                              TextNode(" with no text before", TextType.TEXT)],
                              new_nodes)
        
    def test_no_text_before_link(self):
        node = TextNode("[link](https://i.imgur.com/zjjcJKZ.png) with no text before", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([TextNode("link", TextType.HYPERLINK, "https://i.imgur.com/zjjcJKZ.png"),
                              TextNode(" with no text before", TextType.TEXT)],
                              new_nodes)
                              
    def test_no_text_after_image(self):
        node = TextNode("Testing no text after ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([TextNode("Testing no text after ", TextType.TEXT),
                              TextNode("image", TextType.IMAGE,"https://i.imgur.com/zjjcJKZ.png" )],
                              new_nodes)
        
    def test_no_text_after_link(self):
        node = TextNode("Testing no text after [link](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([TextNode("Testing no text after ", TextType.TEXT),
                              TextNode("link", TextType.HYPERLINK,"https://i.imgur.com/zjjcJKZ.png" )],
                              new_nodes)
        
    def test_multiple_nodes_image(self):
        node1 = TextNode("Testing multiple ![image1](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        node2 = TextNode("And the next ![second image](https://i.imgur.com/3elNhQu.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node1, node2])
        self.assertListEqual([TextNode("Testing multiple ", TextType.TEXT),
                              TextNode("image1", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png" ),
                              TextNode("And the next ", TextType.TEXT),
                              TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png")],
                              new_nodes)
        
    def test_multiple_nodes_link(self):
        node1 = TextNode("Testing multiple [link](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        node2 = TextNode("And the next [second link](https://i.imgur.com/3elNhQu.png)", TextType.TEXT)
        new_nodes = split_nodes_link([node1, node2])
        self.assertListEqual([TextNode("Testing multiple ", TextType.TEXT),
                              TextNode("link", TextType.HYPERLINK, "https://i.imgur.com/zjjcJKZ.png" ),
                              TextNode("And the next ", TextType.TEXT),
                              TextNode("second link", TextType.HYPERLINK, "https://i.imgur.com/3elNhQu.png")],
                              new_nodes)
        

    def test_text_to_textnodes(self):
        sample = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(sample)
        self.assertListEqual([
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.HYPERLINK, "https://boot.dev"),
        ], new_nodes)


    def test_text_to_textnodes_plain(self):
        sample = "This is a plain text sentence to test that the function doesn't break"
        new_nodes = text_to_textnodes(sample)
        self.assertListEqual([TextNode("This is a plain text sentence to test that the function doesn't break", TextType.TEXT)],
                             new_nodes)
        


if __name__ == "__main__":
    unittest.main()