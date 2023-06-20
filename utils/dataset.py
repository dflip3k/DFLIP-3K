import os
import pickle
import json
import shutil
import random
from PIL import Image
import csv
import json
from concurrent.futures import ThreadPoolExecutor
import re

def data_open(s):
    file = open(s,'rb')
    data = pickle.load(file)
    file.close()
    return data

# read images, find corresping in dict(url is important), load scrape info and load png info (if possible),
re_param_code = r'\s*([\w ]+):\s*("(?:\\"[^,]|\\"|\\|[^\"])+"|[^,]*)(?:,|$)'
re_param = re.compile(re_param_code)
re_imagesize = re.compile(r"^(\d+)x(\d+)$")
re_hypernet_hash = re.compile("\(([0-9a-f]+)\)$")

def parse_generation_parameters(x: str):
    res = {}
    prompt = ""
    negative_prompt = ""
    done_with_prompt = False
    *lines, lastline = x.strip().split("\n")
    if len(re_param.findall(lastline)) < 3:
        lines.append(lastline)
        lastline = ''
    for i, line in enumerate(lines):
        line = line.strip()
        if line.startswith("Negative prompt:"):
            done_with_prompt = True
            line = line[16:].strip()
        if done_with_prompt:
            negative_prompt += ("" if negative_prompt == "" else "\n") + line
        else:
            prompt += ("" if prompt == "" else "\n") + line
    res["Prompt"] = prompt
    res["Negative prompt"] = negative_prompt
    others = ""
    for k, v in re_param.findall(lastline):
        if len(v) != 0:
            v = v[1:-1] if v[0] == '"' and v[-1] == '"' else v
            if k in ['Steps','Sampler','CFG scale','Seed','Size','Model hash','Model','Steps','Clip skip','ENSD']:
                res[k] = v
            else:
                others=others+"{}: {} ".format(k, v)
    res['others'] = others
    return res

def parse_novelai(dic):
    jsondict = json.loads(dic['Comment'])
    new_dict = {
        'Prompt': dic['Description'],
        'Negative prompt': jsondict['uc'],
        'Steps': jsondict['steps'],
        'Sampler': jsondict['sampler'],
        'CFG scale': jsondict['scale'],
        'Seed': jsondict['seed'],
        'noise': jsondict['noise'],
        'Model': dic['Software'],
        'Source': dic['Source'],
    }
    return new_dict


parse_data = {}


root = './datasets'
base = "aibooru"
base_root = os.path.join(root, base)
data = data_open(os.path.join(base_root, 'data'))
for imgs in os.listdir(os.path.join(base_root, 'downloads')):
    try:
        image = Image.open(os.path.join(base_root, 'downloads', imgs))
    except:
        print('fail')
    metadata = image.info
    keys = metadata.keys()
    if len(metadata) != 0 and 'icc_profile' not in keys:
        if 'Description' in keys:
            try:
                res = parse_novelai(metadata)
            except:
                print(metadata)
            res['url'] = data[int(imgs.split('.')[0])][1]
            parse_data[os.path.join(base_root, 'downloads', imgs)] = res
        elif 'parameters' in keys:
            try:
                res = parse_generation_parameters(metadata['parameters'])
            except:
                print(metadata)
            res['url'] = data[int(imgs.split('.')[0])][1]
            parse_data[os.path.join(base_root, 'downloads', imgs)] = res

base = "arthub.ai"
base_root = os.path.join(root, base)
data = data_open(os.path.join(base_root, 'data'))
for imgs in os.listdir(os.path.join(base_root, 'downloads')):
    try:
        image = Image.open(os.path.join(base_root, 'downloads', imgs))
    except:
        print('fail')
    res = data[int(imgs.split('.')[0])]
    temp_res = {}
    if 'seed' in res[2].keys():
        temp_res['Seed'] = res[2]['seed']
    elif 'Seed' in res[2].keys():
        temp_res['Seed'] = res[2]['Seed']
    if 'steps' in res[2].keys():
        temp_res['Steps'] = res[2]['steps']
    if 'width' in res[2].keys():
        temp_res['Size'] = str(res[2]['width']) + "x" + str(res[2]['height'])
    elif 'Img Width' in res[2].keys() and 'Img Height' in res[2].keys():
        temp_res['Size'] = str(res[2]['Img Width']) + "x" + str(res[2]['Img Height'])
    elif 'Img Width' in res[2].keys() and 'Img Heigh' in res[2].keys():
        temp_res['Size'] = str(res[2]['Img Width']) + "x" + str(res[2]['Img Heigh'])
    if 'version' in res[2].keys():
        temp_res['Model'] = res[2]['version']
    elif 'model_version' in res[2].keys():
        temp_res['Model'] = res[2]['model_version']
    if 'guidance_scale' in res[2].keys():
        temp_res['CFG scale'] = res[2]['guidance_scale']
    elif 'Scale' in res[2].keys():
        temp_res['CFG scale'] = res[2]['Scale']
    if 'sampler_name' in res[2].keys():
        temp_res['Sampler'] = res[2]['sampler_name']
    if 'Negative' in res[3]:
        new_res = {
            **parse_generation_parameters(res[3]),
            'url': res[1],
            **temp_res,
        }
        print(res)
    else:
        new_res = {
            'Prompt': res[3],
            'url': res[1],
            **temp_res,
        }
    parse_data[os.path.join(base_root, 'downloads', imgs)] = new_res

base = "aigodlike.com"
base_root = os.path.join(root, base)
data = data_open(os.path.join(base_root, 'data'))
for imgs in os.listdir(os.path.join(base_root, 'downloads')):
    try:
        image = Image.open(os.path.join(base_root, 'downloads', imgs))
    except:
        print('fail')
    metadata = image.info
    keys = metadata.keys()
    if len(metadata) != 0 and 'icc_profile' not in keys:
        if 'Description' in keys:
            try:
                res = parse_novelai(metadata)
            except:
                print(metadata)
            res['url'] = data[int(imgs.split('.')[0])][1]
            parse_data[os.path.join(base_root, 'downloads', imgs)] = res
        elif 'parameters' in keys:
            try:
                res = parse_generation_parameters(metadata['parameters'])
            except:
                print(metadata)
            res['url'] = data[int(imgs.split('.')[0])][1]
            parse_data[os.path.join(base_root, 'downloads', imgs)] = res
        else:
            print(imgs)


base = "majinai.art"
base_root = os.path.join(root, base)
with open(os.path.join(root, base,'urls.txt')) as f:
    urls = f.readlines()

urls = [url.strip() for url in urls]

for imgs in os.listdir(os.path.join(base_root, 'downloads')):
    try:
        image = Image.open(os.path.join(base_root, 'downloads', imgs))
    except:
        print('fail')
    metadata = image.info
    keys = metadata.keys()
    if len(metadata) != 0 and 'icc_profile' not in keys:
        if 'Description' in keys:
            try:
                res = parse_novelai(metadata)
            except:
                print(metadata)
            res['url'] = "https://majinai.art/i/{}".format(imgs)
            if res['url'] in urls:
                parse_data[os.path.join(base_root, 'downloads', imgs)] = res
        elif 'parameters' in keys:
            try:
                res = parse_generation_parameters(metadata['parameters'])
            except:
                print(metadata)
            res['url'] = "https://majinai.art/i/{}".format(imgs)
            if res['url'] in urls:
                parse_data[os.path.join(base_root, 'downloads', imgs)] = res
        else:
            print(imgs)


headers = set()
for subdata in parse_data.values():
    headers |= set(subdata.keys())

for key, value in models.items():
    temp_dict = {}
    temp_dict['noise'] = ' '
    temp_dict['Source'] = ' '
    others = ""
    for k, v in value.items():
        if k == 'Size':
            temp_dict['Size'] = v
        elif k == 'ENSD':
            temp_dict['ENSD'] = v
        elif k == 'cfgScale':
            temp_dict['CFG scale'] = v
        elif k == 'Model hash':
            temp_dict['Model hash'] = v
        elif k == 'steps':
            temp_dict['Steps'] = v
        elif k == 'sampler':
            temp_dict['Sampler'] = v
        elif k == 'prompt':
            temp_dict['Prompt'] = v
        elif k == 'Clip skip':
            temp_dict['Clip skip'] = v
        elif k == 'seed':
            temp_dict['Seed'] = v
        elif k == 'Model':
            temp_dict['Model'] = v
        elif k == 'url':
            temp_dict['url'] = v
        elif k == 'negativePrompt':
            temp_dict['Negative prompt'] = v
        else:
            others=others+"{}: {} ".format(k, v)
    temp_dict['others'] = others
    parse_data[key] = temp_dict

headers = set()
for subdata in models.values():
    headers |= set(subdata.keys())






with open("data2.json", "w") as f:
    json.dump(parse_data, f)


save_image_dir = './train'
with open('output.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    allkeys = ['Model', 'Prompt', 'Negative prompt', 'Model hash', 'CFG scale', 'Seed', 'ENSD', 'Steps', 'Sampler', 'Clip skip', 'Size', 'Source', 'noise', 'url', 'others']
    writer.writerow(['file_name', 'Model', 'Prompt', 'Negative prompt', 'Model hash', 'CFG scale', 'Seed', 'ENSD', 'Steps', 'Sampler', 'Clip skip', 'Size', 'Source', 'noise', 'url', 'others'])
    num = 0
    for key, value in parse_data.items():
        num_str = '{:07d}.jpg'.format(num)
        try:
            with Image.open(key) as im:
                im.save(os.path.join(save_image_dir, num_str), quality=80)
        except:
            print(key)
        write_code = [num_str]
        for kk in allkeys:
            if kk in value.keys():
                write_code.append(str(value[kk]))
            else:
                write_code.append(' ')
        writer.writerow(write_code)
        num+=1

####################################################################################################################################
# 指定需要修改的文件夹路径
folder_path = "F:\civitai\mature"

# 遍历文件夹中的所有文件和子文件夹
for root, dirs, files in os.walk(folder_path):
    for filename in files:
        # 判断文件是否没有后缀
        if "." not in filename:
            # 修改文件名，添加后缀为.jpg
            new_filename = filename + ".jpg"
            old_filepath = os.path.join(root, filename)
            new_filepath = os.path.join(root, new_filename)
            os.rename(old_filepath, new_filepath)

folder_path = r'F:\civitai\sfw\download'

models = {}
for filename in os.listdir(folder_path):
    if filename.endswith('.json'):
        filepath = os.path.join(folder_path, filename)
        with open(filepath) as f:
            data = json.load(f)
        if 'meta' in data and data['meta'] is not None:
            if 'Model hash' in data['meta']:
                if data['meta']['Model hash'] in models:
                    models[data['meta']['Model hash']].append(data['id'])
                else:
                    models[data['meta']['Model hash']] = [data['id']]

models = []
# 定义一个函数来处理每个 JSON 文件
def process_json_file(file_path):
    json_path = file_path.split('.')[0]+'.json'
    with open(json_path, 'r') as f:
        data = json.load(f)
    if 'meta' in data and data['meta'] is not None:
        models.append(data)

directory = r'F:\x\download_x'

with ThreadPoolExecutor(max_workers=4) as executor:
    for root, dirs, files in os.walk(directory):
        for file_name in files:
            if file_name.endswith('.png'):
                # 提交任务到线程池
                file_path = os.path.join(root, file_name)
                executor.submit(process_json_file, file_path)
            elif file_name.endswith('.jpg'):
                file_path = os.path.join(root, file_name)
                executor.submit(process_json_file, file_path)


target_dir = r'F:\civitai\models'
for key,val in models.items():
    os.makedirs(os.path.join(target_dir, key), exist_ok=True)
    print(key)
    for v in val:
        shutil.copy(v, os.path.join(target_dir, key, os.path.basename(v)))


target_dir = r'F:\civitai\models_imgnetformat'
for key,val in models.items():
    if len(val)>100:
        random.shuffle(val)
        train_len = len(val)
        os.makedirs(os.path.join(target_dir, 'train', key), exist_ok=True)
        os.makedirs(os.path.join(target_dir, 'val', key), exist_ok=True)
        for v in val[:int(train_len*0.7)]:
            shutil.copy(v, os.path.join(target_dir, 'train', key, os.path.basename(v)))
        for v in val[int(train_len*0.7):]:
            shutil.copy(v, os.path.join(target_dir, 'val', key, os.path.basename(v)))

totoalnum = 0
for key,val in models.items():
    totoalnum+=len(val)


# 定义处理图片的函数
def compress_images(dir_path):
    # 遍历目录下的所有文件和子目录
    for filename in os.listdir(dir_path):
        print(filename)
        # 构造文件或子目录的完整路径
        path = os.path.join(dir_path, filename)
        # 如果是文件，则进行压缩处理
        if os.path.isfile(path):
            # 如果文件格式是jpg或png，则进行压缩处理
            if filename.endswith(".jpg") or filename.endswith(".png"):
                with Image.open(path) as im:
                    # 进行jpg格式的压缩处理
                    if im.format == "PNG":
                        im = im.convert("RGB")
                    im.save(path, optimize=True, quality=95)
        elif os.path.isdir(path):
            compress_images(path)

compress_images(root_dir)

root_dir = '/home/yabin/models_imgnetformat'

for root, dirs, files in os.walk(root_dir):
    for filename in files:
        path = os.path.join(root, filename)
        print(path)
        if filename.endswith(".jpg") or filename.endswith(".png"):
            try:
                with Image.open(path) as im:
                    output_filename = os.path.splitext(path)[0] + '.jpg'
                    im.save(output_filename)
            except:
                print("remove: {}".format(path))
                os.remove(path)

models = {}

def process_json_file(file_path):
    json_path = file_path.split('.')[0]+'.json'
    with open(json_path, 'r') as f:
        data = json.load(f)
    if 'meta' in data and data['meta'] is not None:
        models[file_path] = {'url': data['url'], **data['meta']}

directory = r'F:\civitai\sfw\download'

with ThreadPoolExecutor(max_workers=10) as executor:
    for root, dirs, files in os.walk(directory):
        for file_name in files:
            if file_name.endswith('.png'):
                file_path = os.path.join(root, file_name)
                executor.submit(process_json_file, file_path)
            elif file_name.endswith('.jpg'):
                file_path = os.path.join(root, file_name)
                executor.submit(process_json_file, file_path)


directory = r'F:\civitai\soft\download_soft'

with ThreadPoolExecutor(max_workers=10) as executor:
    for root, dirs, files in os.walk(directory):
        for file_name in files:
            if file_name.endswith('.png'):
                file_path = os.path.join(root, file_name)
                executor.submit(process_json_file, file_path)
            elif file_name.endswith('.jpg'):
                file_path = os.path.join(root, file_name)
                executor.submit(process_json_file, file_path)

############################ DALLE ##########################################
def data_open(s):
    file = open(s,'rb')
    data = pickle.load(file)
    file.close()
    return data


def crop_center(image, width_percent, height_percent):
    original_width, original_height = image.size
    width = original_width * width_percent
    height = original_height * height_percent
    left = (original_width - width) / 2
    top = (original_height - height) / 2
    right = (original_width + width) / 2
    bottom = (original_height + height) / 2
    cropped_image = image.crop((left, top, right, bottom))
    return cropped_image

data = data_open("datasets/dalle/dalle2")
target_dir = './dalle'
root_dir = 'datasets/dalle/downloads'
newdata={}
for num, item in enumerate(data):
    origin_path = os.path.join(root_dir, item[0].split('/')[-1]+'.webp')
    num_str = '{:07d}.jpg'.format(num)
    num_str_c = '{:07d}_1.jpg'.format(num)

    try:
        with Image.open(origin_path) as im:
            im = im.convert('RGB')
            im = crop_center(im, 0.97, 0.97)
            # im.save(os.path.join(target_dir, num_str))
            im.save(os.path.join(target_dir, num_str))
        newdata[os.path.join(target_dir, num_str)] = {
            'url': item[1], 'Prompt':item[2]
        }
    except:
        print(origin_path)

with open("dalle.json", "w") as f:
    json.dump(newdata, f)

























