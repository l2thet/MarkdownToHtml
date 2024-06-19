import unittest

from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode


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
        
    def test_extract_markdown_images(self):
        #Arange
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        
        #Act
        result = HTMLNode.extract_markdown_links(text)
        test = [("link", "https://www.example.com"), ("another", "https://www.example.com/another")]

        #Assert
        self.assertEqual(result, test)   

if __name__ == "__main__":
    unittest.main()