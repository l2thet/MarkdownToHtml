from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None) -> None:
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.tag:
            attribs = self.props_to_html()
            if attribs:
                attribs = " " + attribs
            return f"<{self.tag}{attribs}>{self.value}</{self.tag}>"
        return self.value