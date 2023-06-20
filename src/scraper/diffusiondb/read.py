
# 1st download dataset
import numpy as np
from datasets import load_dataset

# Load the dataset with the `large_random_1k` subset
dataset = load_dataset('poloclub/diffusiondb', '2m_random_10k') # train
dataset = load_dataset('poloclub/diffusiondb', '2m_random_5k') # test

# 2nd extract to download

import os
import shutil
import json

def get_image_files(directory, newdir):
    image_files = []
    for root, dirs, files in os.walk(directory):
        print(files)
        for file in files:
            if os.path.splitext(file)[1].lower() in '.png':
                shutil.copy(os.path.join(root, file),
                            os.path.join(newdir, file))
    return image_files

new_dir = './sd'
image_directory = './extracted'

new_dir = 'datasets/diffusiondb/download'
image_directory = 'datasets/diffusiondb/extracted'
image_files = get_image_files(image_directory, new_dir)


def get_dict(directory):
    image_dict = {}
    for root, dirs, files in os.walk(directory):
        for file in files:
            if os.path.splitext(file)[1].lower() in '.json':
                data = json.load(open(os.path.join(root, file), "r"))
                image_dict.update(data)
    return image_dict

dicts = get_dict(image_directory)

with open("sd.json", "w") as f:
    json.dump(dicts, f)
