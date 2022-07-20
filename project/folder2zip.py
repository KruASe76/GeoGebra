import os
import shutil

def convert(folder_path: str, archive_path: str = None):
    if not archive_path:
        archive_path = folder_path
    try:
        os.remove(f"{folder_path}.zip")
    except FileNotFoundError:
        pass
    shutil.make_archive(archive_path, "zip", folder_path)

if __name__ == "__main__":
    convert(input())