import logging
import re

from src.utils.enums import TextNodeType, MarkdownBlockTypes

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None) -> None:
        self.tag = tag
        self.value = value
        self.children = children or []
        self.props = props if props is not None else {}

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if self.props is None:
            return ""
        props_html = ""
        for prop in self.props:
            props_html += f' {prop}="{self.props[prop]}"'
        return props_html
        
    def children_to_html(self, children = None):
        if children is None:
            children = self.children
        
        # Ensure the base case halts the recursion
        if not children:
            return ""
        
        current_child = children[0]
        rest_of_children = children[1:]
        
        # Recursive call with remaining children, progressively reducing the list
        result = current_child.to_html() + self.children_to_html(rest_of_children)
        
        return result
    
    def __eq__(self, other):
        if not isinstance(other, HTMLNode):
            return False
        return (self.tag == other.tag and
                self.value == other.value and
                self.children == other.children and
                self.props == other.props)
        
    @staticmethod
    def split_nodes_delimiter(old_nodes, delimiter, text_type):
        from src.textnode import TextNode  # Import inside the function to avoid circular reference
        
        new_nodes = []
        for old_node in old_nodes:
            if not isinstance(old_node, TextNode) or old_node.text_type != TextNodeType.TEXT:
                new_nodes.append(old_node)
                continue
            split_nodes = []
            sections = old_node.text.split(delimiter)
            if len(sections) % 2 == 0:
                raise ValueError("Invalid markdown, formatted section not closed")
            for i in range(len(sections)):
                if sections[i] == "":
                    continue
                

                if i % 2 == 0:
                    split_nodes.append(TextNode(sections[i], TextNodeType.TEXT))
                else:
                    split_nodes.append(TextNode(sections[i], text_type))
            new_nodes.extend(split_nodes)
        return new_nodes
    
    @staticmethod
    def split_nodes_image(old_nodes):
        from src.textnode import TextNode  # Import inside the function to avoid circular reference
        
        new_nodes = []
        
        for node in old_nodes:
            if node.text_type != TextNodeType.TEXT:
                new_nodes.append(node)
                continue
            matches = re.finditer(r"!\[(.*?)\]\((.*?)\)", node.text)
            last_end = 0
            for match in matches:
                start, end = match.span()
                if start > last_end:
                    new_nodes.append(TextNode(node.text[last_end:start], TextNodeType.TEXT))
                new_nodes.append(TextNode(match.group(1), TextNodeType.IMAGE, match.group(2)))
                last_end = end
            if last_end < len(node.text):
                new_nodes.append(TextNode(node.text[last_end:], TextNodeType.TEXT))
        
        return new_nodes
    
    @staticmethod
    def split_nodes_link(old_nodes):
        from src.textnode import TextNode  # Import inside the function to avoid circular reference
        
        new_nodes = []
        
        for node in old_nodes:
            if node.text_type != TextNodeType.TEXT:
                new_nodes.append(node)
                continue
            matches = re.finditer(r"\[(.*?)\]\((.*?)\)", node.text)
            last_end = 0
            for match in matches:
                start, end = match.span()
                if start > last_end:
                    new_nodes.append(TextNode(node.text[last_end:start], TextNodeType.TEXT))
                new_nodes.append(TextNode(match.group(1), TextNodeType.LINK, match.group(2)))
                last_end = end
            if last_end < len(node.text):
                new_nodes.append(TextNode(node.text[last_end:], TextNodeType.TEXT))
        
        return new_nodes
    
    @staticmethod
    def text_to_textnodes(text):
        from src.textnode import TextNode  # Import inside the function to avoid circular reference
    
        # Step 1: Initialize the text as a single TextNode
        nodes = [TextNode(text, TextNodeType.TEXT)]
        
        # Step 2: Apply the image splitting function
        nodes = HTMLNode.split_nodes_image(nodes)
        
        # Step 3: Apply the link splitting function
        nodes = HTMLNode.split_nodes_link(nodes)
        
        # Step 4: Apply the delimiter splitting functions for bold, italic, and code
        nodes = HTMLNode.split_nodes_delimiter(nodes, "**", TextNodeType.BOLD)
        nodes = HTMLNode.split_nodes_delimiter(nodes, "*", TextNodeType.ITALIC)
        nodes = HTMLNode.split_nodes_delimiter(nodes, "`", TextNodeType.CODE)
        
        return nodes
    
    @staticmethod
    def markdown_to_blocks(markdown):
        lines = markdown.split("\n")
        results = []
        current_block = []
        
        for line in lines:
            stripped_line = line.strip()
            if stripped_line:
                current_block.append(stripped_line)
            else:
                if current_block:
                    results.append("\n".join(current_block))
                    current_block = []
        
        if current_block:
            results.append("\n".join(current_block))

        return results

    @staticmethod
    def block_to_html_node(block):
        from src.utils.htmlhelpers import HTMLHelpers  # Import inside the function to avoid circular reference
        
        block_type = HTMLHelpers.block_to_block_type(block)
        if block_type == MarkdownBlockTypes.PARAGRAPH:
            return HTMLHelpers.block_paragraph_to_html_node(block)
        if block_type == MarkdownBlockTypes.HEADING:
            return HTMLHelpers.block_heading_to_html_node(block)
        if block_type == MarkdownBlockTypes.CODE:
            return HTMLHelpers.block_code_to_html_node(block)
        if block_type == MarkdownBlockTypes.ORDERED_LIST:
            return HTMLHelpers.block_ordered_list_to_html_node(block)
        if block_type == MarkdownBlockTypes.UNORDERED_LIST:
            return HTMLHelpers.block_unordered_list_to_html_node(block)
        if block_type == MarkdownBlockTypes.QUOTE:
            return HTMLHelpers.block_quote_to_html_node(block)
        raise ValueError("Invalid block type")
    
    @staticmethod
    def markdown_to_html_nodes(markdown):
        from src.htmlnode import HTMLNode
        from src.parentnode import ParentNode
        
        blocks = HTMLNode.markdown_to_blocks(markdown)
        children = []
        for block in blocks:
            html_node = HTMLNode.block_to_html_node(block)
            children.append(html_node)
        return ParentNode("div", children, None)
    
    @staticmethod
    def extract_markdown_images(text: str):
        matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
        return matches
    
    @staticmethod
    def extract_markdown_links(text: str):
        matches = re.findall(r"\[(.*?)\]\((.*?)\)", text)
        return matches
    
    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"