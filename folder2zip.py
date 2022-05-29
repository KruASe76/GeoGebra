import os
import shutil

name = input()

os.remove(f"{name}.zip")
shutil.make_archive(name, "zip", name)
