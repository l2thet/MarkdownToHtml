class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None) -> None:
        self.tag = tag
        self.value = value
        self.children = children or []
        self.props = props if props is not None else {}

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if self.props and isinstance(self.props, dict):
            return ''.join(f"{key}=\"{value}\" " for key, value in self.props.items()).strip()
        else:
            return ""
        
    def children_to_html(self, children):
        if not children:
            return ""
        
        current_child = children[0]
        rest_of_children = children[1:]
        
        return current_child.to_html() + self.children_to_html(rest_of_children)

    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"