import logging
import unittest

from src.htmlnode import HTMLNode
from src.leafnode import LeafNode
from src.parentnode import ParentNode
from src.textnode import TextNode
from src.utils.enums import TextNodeType

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class TestHtmlNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(tag='a', value='link', props={"href": "https://www.google.com", "target": "_blank"})
        expected_result = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), expected_result)

    def test_props_to_html_with_empty_props(self):
        node = HTMLNode()
        expected_result = ''
        self.assertEqual(node.props_to_html(), expected_result)

    def test_to_html_props(self):
        node = HTMLNode(
            "div",
            "Hello, world!",
            None,
            {"class": "greeting", "href": "https://boot.dev"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" href="https://boot.dev"',
        )

    def test_to_html_no_children(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

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

    def test_extract_markdown_images(self):
        #Arange
        text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
        
        #Act
        result = HTMLNode.extract_markdown_images(text)
        test = [("image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"), ("another", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png")]

        #Assert
        self.assertEqual(result, test)
        
    def test_extract_markdown_links(self):
        #Arange
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        
        #Act
        result = HTMLNode.extract_markdown_links(text)
        test = [("link", "https://www.example.com"), ("another", "https://www.example.com/another")]

        #Assert
        self.assertEqual(result, test)
        
    def test_split_nodes_image_returns_expected_result(self):
        # Arrange
        old_nodes = TextNode(
            "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
            TextNodeType.TEXT,
        )
        
        expected_result = [
                            TextNode("This is text with an ", TextNodeType.TEXT),
                            TextNode("image", TextNodeType.IMAGE, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
                            TextNode(" and another ", TextNodeType.TEXT),
                            TextNode(
                                "second image", TextNodeType.IMAGE, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png"
                            ),
                        ]
        
        # Act
        result = HTMLNode.split_nodes_image([old_nodes])
        logging.debug(f"result: {result}")
        
        # Assert
        self.assertEqual(result, expected_result)
        
    def test_split_nodes_links_returns_expected_result(self):
        # Arrange
        old_nodes = TextNode(
            "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
            TextNodeType.TEXT,
        )
        
        expected_result = [
                            TextNode("This is text with an ", TextNodeType.TEXT),
                            TextNode("image", TextNodeType.IMAGE, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
                            TextNode(" and another ", TextNodeType.TEXT),
                            TextNode(
                                "second image", TextNodeType.IMAGE, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png"
                            ),
                        ]
        
        # Act
        result = HTMLNode.split_nodes_image([old_nodes])
        logging.debug(f"result: {result}")
        
        # Assert
        self.assertEqual(result, expected_result)
        
    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextNodeType.TEXT,
        )
        new_nodes = HTMLNode.split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextNodeType.TEXT),
                TextNode("image", TextNodeType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.com/image.png)",
            TextNodeType.TEXT,
        )
        new_nodes = HTMLNode.split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextNodeType.IMAGE, "https://www.example.com/image.png"),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextNodeType.TEXT,
        )
        new_nodes = HTMLNode.split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextNodeType.TEXT),
                TextNode("image", TextNodeType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextNodeType.TEXT),
                TextNode(
                    "second image", TextNodeType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
            TextNodeType.TEXT,
        )
        new_nodes = HTMLNode.split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextNodeType.TEXT),
                TextNode("link", TextNodeType.LINK, "https://boot.dev"),
                TextNode(" and ", TextNodeType.TEXT),
                TextNode("another link", TextNodeType.LINK, "https://blog.boot.dev"),
                TextNode(" with text that follows", TextNodeType.TEXT),
            ],
            new_nodes,
        )
        
    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"
        text_nodes = HTMLNode.text_to_textnodes(text)
        
        compare = [
            TextNode("This is ", TextNodeType.TEXT),
            TextNode("text", TextNodeType.BOLD),
            TextNode(" with an ", TextNodeType.TEXT),
            TextNode("italic", TextNodeType.ITALIC),
            TextNode(" word and a ", TextNodeType.TEXT),
            TextNode("code block", TextNodeType.CODE),
            TextNode(" and an ", TextNodeType.TEXT),
            TextNode("image", TextNodeType.IMAGE, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(" and a ", TextNodeType.TEXT),
            TextNode("link", TextNodeType.LINK, "https://boot.dev"),
        ]
        
        self.assertListEqual(text_nodes, compare)
        
    def test_markdown_to_blocks(self):
        markdown_string = """This is **bolded** paragraph

            This is another paragraph with *italic* text and `code` here
            This is the same paragraph on a new line

            * This is a list
            * with items
            """
        result = HTMLNode.markdown_to_blocks(markdown_string)
        
        compare = [
                    "This is **bolded** paragraph",
                    "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                    "* This is a list\n* with items"
                ]
        
        self.assertListEqual(result, compare)
        
    def test_markdown_to_blocks(self):
        md = """
        This is **bolded** paragraph

        This is another paragraph with *italic* text and `code` here
        This is the same paragraph on a new line

        * This is a list
        * with items
        """
        blocks = HTMLNode.markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
        This is **bolded** paragraph




        This is another paragraph with *italic* text and `code` here
        This is the same paragraph on a new line

        * This is a list
        * with items
        """
        blocks = HTMLNode.markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )
            
if __name__ == "__main__":
    unittest.main()