import os
import hashlib
import os
from PIL import Image

# 设置输入和输出文件夹路径
input_dir = 'downloads'
output_dir = './aigodlike_downloads_webp'

# 遍历文件夹中所有PNG文件
for filename in os.listdir(input_dir):
    if filename.endswith('.png'):
        # 打开PNG文件
        with Image.open(os.path.join(input_dir, filename)) as im:
            # 将PNG转换成WebP，并将输出保存到另一个文件夹中
            output_filename = os.path.splitext(filename)[0] + '.webp'
            output_path = os.path.join(output_dir, output_filename)
            im.save(output_path, 'webp')
