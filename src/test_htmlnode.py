import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )

        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )

if __name__ == "__main__":
    unittest.main()