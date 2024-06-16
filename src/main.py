from textnode import TextNode
from utils.enums import TextType

def main():        
    result = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
    print(result)

if __name__ == "__main__":
    main()