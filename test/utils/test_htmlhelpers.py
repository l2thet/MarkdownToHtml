import unittest

from src.htmlnode import HTMLNode
from src.utils.enums import MarkdownBlockTypes
from src.utils.htmlhelpers import HTMLHelpers


class TestHtmlHelpers(unittest.TestCase):
    
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

    def test_block_to_block_type(self):
        self.assertEqual(
            HTMLHelpers.block_to_block_type("This is a paragraph"),
            MarkdownBlockTypes.PARAGRAPH,
        )
        self.assertEqual(
            HTMLHelpers.block_to_block_type("# This is a heading"),
            MarkdownBlockTypes.HEADING,
        )
        self.assertEqual(
            HTMLHelpers.block_to_block_type("> This is a quote"),
            MarkdownBlockTypes.QUOTE,
        )
        self.assertEqual(
            HTMLHelpers.block_to_block_type("```This is a code block```"),
            MarkdownBlockTypes.CODE,
        )
        self.assertEqual(
            HTMLHelpers.block_to_block_type("- This is an unordered list"),
            MarkdownBlockTypes.UNORDERED_LIST,
        )
        self.assertEqual(
            HTMLHelpers.block_to_block_type("1. This is an ordered list"),
            MarkdownBlockTypes.ORDERED_LIST,
        )
        
    def test_block_quote_to_html_node(self):
        input_block = ['> This is a quote']
        
        block = HTMLNode("blockquote", value="This is a quote")
        
        result = HTMLHelpers.block_quote_to_html_node(input_block)
        
        self.assertEqual(block, result)

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

    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(HTMLHelpers.block_to_block_type(block), MarkdownBlockTypes.HEADING)
        block = "```\ncode\n```"
        self.assertEqual(HTMLHelpers.block_to_block_type(block), MarkdownBlockTypes.CODE)
        block = "> quote\n> more quote"
        self.assertEqual(HTMLHelpers.block_to_block_type(block), MarkdownBlockTypes.QUOTE)
        block = "* list\n* items"
        self.assertEqual(HTMLHelpers.block_to_block_type(block), MarkdownBlockTypes.UNORDERED_LIST)
        block = "1. list\n2. items"
        self.assertEqual(HTMLHelpers.block_to_block_type(block), MarkdownBlockTypes.ORDERED_LIST)
        block = "paragraph"
        self.assertEqual(HTMLHelpers.block_to_block_type(block), MarkdownBlockTypes.PARAGRAPH)

    # def test_paragraph(self):
    #     md = """
    #     This is **bolded** paragraph
    #     text in a p
    #     tag here

    #     """

    #     node = HTMLNode.markdown_to_html_nodes(md)
    #     html = node.to_html()
    #     self.assertEqual(
    #         html,
    #         "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
    #     )

    # def test_lists(self):
    #     md = """
    #     - This is a list
    #     - with items
    #     - and *more* items

    #     1. This is an `ordered` list
    #     2. with items
    #     3. and more items

    #     """

    #     node = HTMLNode.markdown_to_html_nodes(md)
    #     html = node.to_html()
    #     self.assertEqual(
    #         html,
    #         "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
    #     )

    # def test_headings(self):
    #     md = """
    #     # this is an h1

    #     this is paragraph text

    #     ## this is an h2
    #     """

    #     node = HTMLNode.markdown_to_html_nodes(md)
    #     html = node.to_html()
    #     self.assertEqual(
    #         html,
    #         "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
    #     )

    # def test_blockquote(self):
    #     md = """
    #     > This is a
    #     > blockquote block

    #     this is paragraph text

    #     """

    #     node = HTMLNode.markdown_to_html_nodes(md)
    #     html = node.to_html()
    #     self.assertEqual(
    #         html,
    #         "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
    #     )   
        
if __name__ == "__main__":
    unittest.main()