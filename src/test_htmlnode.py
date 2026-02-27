from htmlnode import HTMLNode, LeafNode,ParentNode
import unittest

class TestHTMLNode(unittest.TestCase):
    def test_props(self):
        node = HTMLNode(props = {"href": "www.google.com", "target": "_blank" })
        node2 = HTMLNode(props = {})
        self.assertEqual(node.props_to_html(), ' href="www.google.com" target="_blank"')
        self.assertEqual(node2.props_to_html(), '')

    def test_to_html(self):
        node = HTMLNode()
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_all_values(self):
        child_node = HTMLNode(tag="p")
        node = HTMLNode(tag="header", value="This is just a test", children=[child_node], props={"key":"value"})

        self.assertEqual(node.tag, "header")
        self.assertEqual(node.value, "This is just a test")
        self.assertEqual(node.children, [child_node])
        self.assertEqual(node.props, {"key":"value"} )

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Link", {'href': 'https://www.google.com'})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Link</a>')

    def test_leaf_repr(self):
        node = LeafNode("b", "Just a test", {"next":"step" })
        self.assertEqual(node.__repr__(), "Tag = b, Value = Just a test, Props = {'next': 'step'}")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
    )
    
    def test_to_html_great_grandchild(self):
        great_grand = LeafNode("i", "italic test")
        grand_child = ParentNode("p", [great_grand])
        child = ParentNode("ol", [grand_child])
        parent = ParentNode("h1", [child])
        self.assertEqual(parent.to_html(), "<h1><ol><p><i>italic test</i></p></ol></h1>")

    def test_parent_to_html_no_tag_raises(self):
        node = ParentNode(None, [LeafNode(None, "x")])
        with self.assertRaises(ValueError) as m:
            node.to_html()
        self.assertEqual(str(m.exception), "No tag")

    def test_parent_to_html_no_child_raises(self):
        node = ParentNode("a", None)
        with self.assertRaises(ValueError) as m:
            node.to_html()
        self.assertEqual(str(m.exception), "Missing child value")

    def test_parent_multiple_children(self):
        node = ParentNode("p", [LeafNode(None, "test"), 
                                LeafNode("i", "more tests"),
                                LeafNode("p", "final"),
                                ])
        self.assertEqual(node.to_html(), "<p>test<i>more tests</i><p>final</p></p>")

    def test_parent_props(self):
        node = ParentNode("div", [LeafNode(None, "x")], {"class": "box"})
        self.assertEqual(node.to_html(), '<div class="box">x</div>')




if __name__ == "__main__":
    unittest.main()