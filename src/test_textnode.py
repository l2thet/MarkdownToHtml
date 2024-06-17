import unittest

from textnode import TextNode
from utils.enums import TextNodeType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextNodeType.TEXT)
        node2 = TextNode("This is a text node", TextNodeType.TEXT)
        self.assertEqual(node, node2)

    def test_eq_false(self):
        node = TextNode("This is a text node", TextNodeType.TEXT)
        node2 = TextNode("This is a text node", TextNodeType.BOLD)
        self.assertNotEqual(node, node2)

    def test_eq_false2(self):
        node = TextNode("This is a text node", TextNodeType.TEXT)
        node2 = TextNode("This is a text node2", TextNodeType.TEXT)
        self.assertNotEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a text node", TextNodeType.TEXT, "https://www.boot.dev")
        node2 = TextNode("This is a text node", TextNodeType.TEXT, "https://www.boot.dev")
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextNodeType.TEXT, "https://www.boot.dev")
        self.assertEqual(
            "TextNode(This is a text node, text, https://www.boot.dev)", repr(node)
        )



if __name__ == "__main__":
    unittest.main()