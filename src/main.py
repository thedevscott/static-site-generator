import os
import shutil
import sys
import textnode as tn

from textnode import (
    copy_static_to_public,
    generate_page,
    generate_pages_recursive,
)

static_dir = "./static"
public_dir = "./docs"
content_dir = "./content"
template_path = "./template.html"
default_base = "/"

def main():
    basepath = default_base

    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    print("Deleting public directory...")
    if os.path.exists(public_dir):
        shutil.rmtree(public_dir)
    
    print("Copying static contents to public directory")
    copy_static_to_public(static_dir, public_dir)

    print("Generating content...")
    generate_pages_recursive(content_dir, template_path, public_dir, basepath)

if __name__ == '__main__':
    main()