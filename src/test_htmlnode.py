import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_value(self):
        node1 = HTMLNode("div", "Some div text here",)
        self.assertEqual(node1.tag, "div")
        self.assertEqual(node1.value, "Some div text here")
    
    def test_props(self):
        node1 = HTMLNode(None, None, None, {"href": "https://www.google.com","target": "_blank",})
        self.assertEqual(node1.props_to_html(), f" href=\"https://www.google.com\" target=\"_blank\"")

    def test_obj_repr(self):
        node1 = HTMLNode("div", "Hello world div", None, {"target": "_blank"})
        self.assertEqual(node1.__repr__(), "HTMLNode(div, Hello world div, children: None, {'target': '_blank'})")

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, World!")
        self.assertEqual(node.to_html(), "<p>Hello, World!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click here", {"href": "http://www.example.com","target": "_blank"})
        self.assertEqual(node.to_html(), f"<a href=\"http://www.example.com\" target=\"_blank\">Click here</a>")

if __name__ == "__main__":
    unittest.main()