import unittest

from textnode import TextNode, TextType, text_node_to_html_node 


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

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("Let's test bold", TextType.BOLD )
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Let's test bold")

    def test_link(self):
        node = TextNode("Prepare for hyperspace", TextType.HYPERLINK, "www.blastoff.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Prepare for hyperspace")
        self.assertEqual(html_node.props, {"href":"www.blastoff.com"})

    def test_img(self):
        node = TextNode("New image", TextType.IMAGE, "www.imagesite.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props["src"], "www.imagesite.com")
        self.assertEqual(html_node.props["alt"], "New image")

if __name__ == "__main__":
    unittest.main()