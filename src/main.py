import os
import shutil

from textnode import TextNode
from utils.enums import TextNodeType

def main():        
    result = TextNode("This is a text node", TextNodeType.BOLD, "https://www.boot.dev")
    print(result)
    if os.path.exists("../public"):
        shutil.rmtree("../public", ignore_errors=True)
    cp_folder_recursive("../static", "../public")


def cp_folder_recursive(folder_source, folder_dest):
    # Copy all the files in the folder_sorce to folder_dest and all the files in the subfolders
    if folder_source == folder_dest:
        return
    if os.path.exists(folder_source):
        for item in os.listdir(folder_source):
            item_path = os.path.join(folder_source, item)
            if os.path.isdir(item_path):
                cp_folder_recursive(item_path, os.path.join(folder_dest, item))
            else:
                if not os.path.exists(folder_dest):
                    os.makedirs(folder_dest)
                with open(item_path, 'rb') as f:
                    with open(os.path.join(folder_dest, item), 'wb') as f1:
                        f1.write(f.read())

if __name__ == "__main__":
    main()