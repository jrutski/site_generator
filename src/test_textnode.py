import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_missing_url(self):
        node = TextNode("This is a text node", TextType.ITALIC, "http://www.example.com")
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_text_diff(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node2", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_obj_repr(self):
        node = TextNode("This is a text node", TextType.BOLD, "http://www.example.com")
        self.assertEqual("TextNode(This is a text node, bold, http://www.example.com)", repr(node))

if __name__ == "__main__":
    unittest.main()
