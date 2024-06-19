import unittest

from parentnode import ParentNode
from leafnode import LeafNode


class TestParentNode(unittest.TestCase):
    def test_to_html(self):
        
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ])
        
        node_expected_result = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        
        self.assertEqual(node.to_html(), node_expected_result)

if __name__ == "__main__":
    unittest.main()