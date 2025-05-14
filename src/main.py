import os, shutil
import textnode as tn

from textnode import copy_static_to_public

static_dir = "./static"
public_dir = "./public"

def main():
    print("Deleting public directory...")
    if os.path.exists(public_dir):
        shutil.rmtree(public_dir)
    
    print("Copying static contents to public directory")
    copy_static_to_public(static_dir, public_dir)


if __name__ == '__main__':
    main()