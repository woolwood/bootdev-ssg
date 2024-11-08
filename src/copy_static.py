import os
import shutil


def copy_over_files(src, dst):
    src_files = os.listdir(src)
    if os.path.exists(dst):
        shutil.rmtree(dst)
        print(f"Destination exists, deleting {dst}")
    os.mkdir(dst)
    print(f"Creating {dst}")

    for filename in src_files:
        filepath = os.path.join(src, filename)
        if os.path.isfile(filepath):
            shutil.copy2(filepath, dst)
            print(f"Copied {filepath} to {dst}")
        if os.path.isdir(filepath):
            dest_filepath = os.path.join(dst, filename)
            print(f"{filepath} is directory, creating {dest_filepath}")
            copy_over_files(filepath, dest_filepath)
