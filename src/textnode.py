from src.leafnode import LeafNode
from src.utils.enums import TextNodeType


class TextNode:
    def __init__(self, text, text_type: TextNodeType, url = None) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, value: object) -> bool:
        return (
            self.text == value.text
            and self.text_type == value.text_type
            and self.url == value.url
        )
    
    def text_node_to_html_node(self, text_node):
        match text_node:
            case TextNodeType.TEXT:
                return LeafNode(None, self.text)
            case TextNodeType.BOLD:
                return LeafNode("b", self.text)
            case TextNodeType.ITALIC:
                return LeafNode("i", self.text)
            case TextNodeType.CODE:
                return LeafNode("code", self.text)
            case TextNodeType.LINK:
                return LeafNode("a", text_node.text, {"href": text_node.url})
            case TextNodeType.IMAGE:
                return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
            case _:
                raise ValueError(f"Invalid text type: {self.text_type}")
    
    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
    