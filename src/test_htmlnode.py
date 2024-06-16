import unittest

from htmlnode import HTMLNode
#from textnode import TextNode
#from utils.enums import TextType


class TestHtmlNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(tag='a', value='link', props={"href": "https://www.google.com", "target": "_blank"})
        expected_result = 'href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), expected_result)


if __name__ == "__main__":
    unittest.main()