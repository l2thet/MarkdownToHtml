import logging

from utils.enums import TextNodeType

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

    # @staticmethod
    # def split_nodes_delimiter(old_nodes, delimiter, text_node_type):
    #     from textnode import TextNode  # Import inside the function to avoid circular reference

    #     results = []
    #     for node in old_nodes:
    #         if isinstance(node, TextNode) and node.text_type == TextNodeType.CODE:
    #             parts = node.text.split(delimiter)
    #             for index, part in enumerate(parts):
    #                 if part:
    #                     if index % 2 == 0:
    #                         results.append(TextNode(part, TextNodeType.TEXT))
    #                     else:
    #                         results.append(TextNode(part, TextNodeType.CODE))
    #         elif isinstance(node, TextNode) and node.text_type == TextNodeType.BOLD:
    #             parts = node.text.split(delimiter)
    #             logging.debug(f"Parts: {parts}")
    #             for index, part in enumerate(parts):
    #                 if part:
    #                     if index % 2 == 0:
    #                         results.append(TextNode(part, TextNodeType.TEXT))
    #                     else:
    #                         results.append(TextNode(part, TextNodeType.BOLD))
    #         elif isinstance(node, TextNode) and node.text_type == TextNodeType.ITALIC:
    #             parts = node.text.split(delimiter)
    #             for index, part in enumerate(parts):
    #                 if part:
    #                     if index % 2 == 0:
    #                         results.append(TextNode(part, TextNodeType.TEXT))
    #                     else:
    #                         results.append(TextNode(part, TextNodeType.ITALIC))
    #         else:
    #             results.append(node)

    #     return results
    
    @staticmethod
    def split_nodes_delimiter(old_nodes, delimiter, text_type):
        from textnode import TextNode  # Import inside the function to avoid circular reference
        
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
    
    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"