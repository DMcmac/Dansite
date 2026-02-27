import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_url(self):
        node = TextNode("Need to check the url", TextType.HYPERLINK,)
        node2 = TextNode("Need to check the url", TextType.HYPERLINK, "www.google.com" )
        self.assertNotEqual(node, node2)

    def test_type(self):
        node = TextNode("Does the type match", TextType.BOLD,)
        node2 = TextNode("Does the type match", TextType.ITALIC)
        self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()