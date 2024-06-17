from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None) -> None:
        super().__init__(tag, value, None, props)

    def to_html(self):
        attribs = ""
        if self.props:
            attribs = ' ' + ''.join(f"{key}=\"{value}\"" for key, value in self.props.items()).strip()
        if self.value:
            if self.tag is None:
                return self.value
            return f"<{self.tag}{attribs}>{self.value}</{self.tag}>"
        else:
            raise ValueError()