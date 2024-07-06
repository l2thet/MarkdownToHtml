from src.htmlnode import HTMLNode
from src.inline_markdown import text_to_textnodes
from src.textnode import text_node_to_html_node
from src.parentnode import ParentNode
from src.textnode import TextNode
from src.utils.enums import MarkdownBlockTypes


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)
    
def block_to_html_node(block): 
    block_type = block_to_block_type(block)
    if block_type == MarkdownBlockTypes.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == MarkdownBlockTypes.HEADING:
        return heading_to_html_node(block)
    if block_type == MarkdownBlockTypes.CODE:
        return code_to_html_node(block)
    if block_type == MarkdownBlockTypes.ORDERED_LIST:
        return olist_to_html_node(block)
    if block_type == MarkdownBlockTypes.UNORDERED_LIST:
        return ulist_to_html_node(block)
    if block_type == MarkdownBlockTypes.QUOTE:
        return quote_to_html_node(block)
    raise ValueError("Invalid block type")

def block_to_block_type(block):
    lines = block.split("\n")

    if (
        block.startswith("# ")
        or block.startswith("## ")
        or block.startswith("### ")
        or block.startswith("#### ")
        or block.startswith("##### ")
        or block.startswith("###### ")
    ):
        return MarkdownBlockTypes.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return MarkdownBlockTypes.CODE
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return MarkdownBlockTypes.PARAGRAPH
        return MarkdownBlockTypes.QUOTE
    if block.startswith("* "):
        for line in lines:
            if not line.startswith("* "):
                return MarkdownBlockTypes.PARAGRAPH
        return MarkdownBlockTypes.UNORDERED_LIST
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return MarkdownBlockTypes.PARAGRAPH
        return MarkdownBlockTypes.UNORDERED_LIST
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return MarkdownBlockTypes.PARAGRAPH
            i += 1
        return MarkdownBlockTypes.ORDERED_LIST
    return MarkdownBlockTypes.PARAGRAPH

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"Invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid code block")
    text = block[4:-3]
    children = text_to_children(text)
    code = ParentNode("code", children)
    return ParentNode("pre", [code])


def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)