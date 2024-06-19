import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        node = LeafNode("p", "This is a paragraph of text.")
        node2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        node_expected_result = "<p>This is a paragraph of text.</p>"
        node2_expected_result = '<a href="https://www.google.com">Click me!</a>'
        
        self.assertEqual(node.to_html(), node_expected_result)
        self.assertEqual(node2.to_html(), node2_expected_result)

if __name__ == "__main__":
    unittest.main()