from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None) -> None:
        super().__init__(tag, None, children, props)

    def to_html(self):
        attribs = ""
        result = ""

        if self.tag is None:
            raise ValueError("Tag cannot be empty")
        if not self.children:
            raise ValueError("Children prop cannot be empty")
        if self.props:
            attribs = self.props_to_html()
        result = f"<{self.tag}{attribs}>"
        result += self.children_to_html()
        result += f"</{self.tag}>"
        return result