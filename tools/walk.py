# This script walks in a littlefs image and print contents.
#
# E.g.
# % python3 examples/walk.py --img-filename=test.img
# root . dirs ['lfs'] files ['test_directories.py', 'test_files.py', 'test_remove_rename.py', 'test_version.py', 'test_walk.py']
# root ./lfs dirs [] files ['conftest.py', 'test_dir_functions.py', 'test_file_functions.py', 'test_fs_functions.py']
# %

import argparse

from littlefs import LittleFS

parser = argparse.ArgumentParser()
parser.add_argument("--img-filename", default="build/littlefs.img")

args = parser.parse_args()

img_filename = args.img_filename
# same magic numbers as in tools\filesystem_generate.py
block_size = 4096
block_count = 512
prog_size = 256
disk_version: int = 0x00020000


fs = LittleFS(
    block_size=block_size,
    block_count=block_count,
    prog_size=prog_size,
    disk_version=disk_version,
)

with open(img_filename, "rb") as f:
    data = f.read()

if len(data) / block_size != block_count:
    print("image size error: should be a multiple of block size")
    exit(1)

fs.context.buffer = bytearray(data)
fs.mount()

for root, dirs, files in fs.walk("."):
    print(f"root {root} dirs {dirs} files {files}")
