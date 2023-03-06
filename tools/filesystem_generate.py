import os
from littlefs import LittleFS
import subprocess

workspace_dir = '/workspace'

files = os.listdir(f"{workspace_dir}/src")

output_image = f"{workspace_dir}/output/littlefs.img"

lfs = LittleFS(block_size=4096, block_count=512, prog_size=256)

for filename in files:
    with open(f"{workspace_dir}/src/{filename}", 'rb') as src_file:
        with  lfs.open(filename, 'wb') as lfs_file:
            lfs_file.write(src_file.read())

with open(output_image, 'wb') as fh:
    fh.write(lfs.context.buffer)

subprocess.run(f"esptool.py --chip esp32 merge_bin -o {workspace_dir}/output/out.bin --flash_mode dio --flash_size 4MB 0x1000 {workspace_dir}/firmware/esp32-20220618-v1.19.1.bin 0x200000 {workspace_dir}/output/littlefs.img", shell=True)