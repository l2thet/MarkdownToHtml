from src.parentnode import ParentNode
from src.utils.enums import MarkdownBlockTypes


class HTMLHelpers:
    @staticmethod
    def block_to_block_type(block):
        if block.startswith("#"):
            return MarkdownBlockTypes.HEADING
        if block.startswith(">"):
            return MarkdownBlockTypes.QUOTE
        if block.startswith("```"):
            return MarkdownBlockTypes.CODE
        if block.startswith("- ") or block.startswith("* "):
            return MarkdownBlockTypes.UNORDERED_LIST
        if block.startswith("1. "):
            return MarkdownBlockTypes.ORDERED_LIST
        return MarkdownBlockTypes.PARAGRAPH
    
    @staticmethod
    def block_quote_to_html_node(block):
        from src.htmlnode import HTMLNode
        result = HTMLNode("blockquote", value=block[0][1:].strip()) 
        return result
    
    @staticmethod
    def block_heading_to_html_node(block):
        from src.htmlnode import HTMLNode
        level = len(block[0].split(" ")[0])
        result = HTMLNode(f"h{level}", value=block[0][level:].strip())
        return result
    
    @staticmethod
    def block_code_to_html_node(block):
        from src.htmlnode import HTMLNode
        result = HTMLNode("code", value=block[1:])
        return result
    
    staticmethod
    def block_unordered_list_to_html_node(block):
        from src.htmlnode import HTMLNode
        result = HTMLNode("ul")
        for line in block:
            result.children.append(HTMLNode("li", value=line[2:].strip()))
        return result
    
    @staticmethod
    def block_ordered_list_to_html_node(block):
        from src.htmlnode import HTMLNode
        result = HTMLNode("ol")
        for line in block:
            result.children.append(HTMLNode("li", value=line[3:].strip()))
        return result
    
    @staticmethod
    def block_paragraph_to_html_node(block):
        from src.htmlnode import HTMLNode
        
        result = HTMLNode("p", value=block[0])
        return result
    
    
    
    