import shutil
import os
from config import VERBOSE

def verbose(text):
    if VERBOSE: print(text)

def get_treemap(target:str):
    treemap = {}
    if not target:
        return None
    dirs = os.listdir(target)
    for dir in dirs:
        dir_path = os.path.join(target, dir)
        if os.path.isfile(dir_path):
            treemap[dir] = None
        else:
            treemap[dir] = get_treemap(dir_path)
    return treemap

def copy_from_treemap(src, dst, treemap:dict, level=0):
    for key, value in treemap.items():
        dst_path = os.path.join(dst, key)
        src_path = os.path.join(src, key)
        if type(value) is dict:
            verbose(f"{' '*(level)*2}+{key}")
            os.mkdir(dst_path)
            copy_from_treemap(src_path, dst_path, value, level+1)
        elif value is None:
            verbose(f"{' '*level*2}|{key}")
            shutil.copy(src_path, dst_path)
        else:
            raise ValueError(f"Unexpected tree value at \"{key}\"")

def copy_static(dst:str):
    if os.path.exists(dst):
        shutil.rmtree(dst)
    if os.path.exists(dst):
        raise RuntimeError(f"Failed to delete .{dst} directory")
    os.mkdir(dst)
    if not os.path.exists("static"):
        raise RuntimeError("\"static\" directory not found")
    treemap = get_treemap("static")
    copy_from_treemap("static", dst, treemap)


if __name__ == "__main__":
    print("Copying from static...")
    copy_static()
    print("\nCopy Completed")
        

