import logging
import unittest

from src.inline_markdown import split_nodes_delimiter
from src.textnode import TextNode
from src.utils.enums import TextNodeType
from src.htmlnode import HTMLNode


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
            "TextNode(This is a text node, TextNodeType.TEXT, https://www.boot.dev)", repr(node)
        )

    def test_split_nodes_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextNodeType.TEXT)
        node2 = [
                    TextNode("This is text with a ", TextNodeType.TEXT),
                    TextNode("code block", TextNodeType.CODE),
                    TextNode(" word", TextNodeType.TEXT),
                ]

        node_split = split_nodes_delimiter([node], "`", TextNodeType.CODE)

        self.assertEqual(node_split, node2)

    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextNodeType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextNodeType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextNodeType.TEXT),
                TextNode("bolded", TextNodeType.BOLD),
                TextNode(" word", TextNodeType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextNodeType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextNodeType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextNodeType.TEXT),
                TextNode("bolded", TextNodeType.BOLD),
                TextNode(" word and ", TextNodeType.TEXT),
                TextNode("another", TextNodeType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextNodeType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextNodeType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextNodeType.TEXT),
                TextNode("bolded word", TextNodeType.BOLD),
                TextNode(" and ", TextNodeType.TEXT),
                TextNode("another", TextNodeType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an *italic* word", TextNodeType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextNodeType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextNodeType.TEXT),
                TextNode("italic", TextNodeType.ITALIC),
                TextNode(" word", TextNodeType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and *italic*", TextNodeType.TEXT)
        bold_node = split_nodes_delimiter([node], "**", TextNodeType.BOLD)
        new_nodes = split_nodes_delimiter(bold_node, "*", TextNodeType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextNodeType.BOLD),
                TextNode(" and ", TextNodeType.TEXT),
                TextNode("italic", TextNodeType.ITALIC),
            ],
            new_nodes,
        )

if __name__ == "__main__":
    unittest.main()