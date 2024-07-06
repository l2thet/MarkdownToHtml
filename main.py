import os
import shutil

from src.gencontent import generate_page
from src.textnode import TextNode
from src.utils.enums import TextNodeType

dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"
template_path = "./template.html"

def main():        
    result = TextNode("This is a text node", TextNodeType.BOLD, "https://www.boot.dev")
    print(result)
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public, ignore_errors=True)
    cp_folder_recursive(dir_path_static, dir_path_public)
    
    generate_page(
        os.path.join(dir_path_content, "index.md"),
        template_path,
        os.path.join(dir_path_public, "index.html"),
    )


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