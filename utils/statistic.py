import os
import pickle
import json
import shutil
import random
from PIL import Image
import csv
import re
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(font="Times New Roman")


def data_open(s):
    file = open(s,'rb')
    data = pickle.load(file)
    file.close()
    return data


def g_num_rawsamples():
    num = 0
    root = './datasets'
    base = "aibooru"
    base_root = os.path.join(root, base)
    data = data_open(os.path.join(base_root, 'data'))
    num+=len(data)
    base = "arthub.ai"
    base_root = os.path.join(root, base)
    data = data_open(os.path.join(base_root, 'data'))
    num+=len(data)
    base = "aigodlike.com"
    base_root = os.path.join(root, base)
    data = data_open(os.path.join(base_root, 'data'))
    num+=len(data)
    base = "majinai.art"
    with open(os.path.join(root, base,'urls.txt')) as f:
        urls = f.readlines()
    num+=len(urls)

    def count_images_oswalk(dir_path):
        IMAGE_EXTS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp'}
        count = 0
        for root, dirs, files in os.walk(dir_path):
            for filename in files:
                filepath = os.path.join(root, filename)
                ext = os.path.splitext(filepath)[1].lower()
                if ext in IMAGE_EXTS:
                    count += 1
        return count
    num_images = count_images_oswalk("F:\civitai")
    num+=num_images
    return num

# 最初搜索的图片
num_rawsamples = g_num_rawsamples()


# 筛选后，有prompt的图片数量，和图片选择
def get_image_w_prompt():
    files = os.listdir('datasets/dddb/0_real')
    print("real image number: {}".format(len(files)))

    # Dalle
    dalle_wP,dalle_woP = 0,0
    dalle_dataset = json.load(open("processeddata/dalle.json", "r"))
    for key,value in dalle_dataset.items():
        text = value['Prompt']
        if text is not None:
            dalle_wP += 1
        else:
            dalle_woP+=1
    print("dalle image with prompt number: {}".format(dalle_wP))
    print("dalle image without prompt number: {}".format(dalle_woP))

    # Midjourney
    mj_wP,mj_woP = 0,0
    data = json.load(open("processeddata/mj_up.json", "r"))
    root_dir = "datasets/mj/downloads"
    files = os.listdir(root_dir)
    for i, file_name in enumerate(files):
        key = 'mj/' + file_name
        values = data[key]
        input_string = values["Prompt"]
        cleaned_string = re.sub(r'<[^>]+>', '', input_string)
        cleaned_string = re.sub(r'\s*--[^\s\d]+(?:\s+\d+:\d+)*', '', cleaned_string)
        cleaned_string = re.sub(r'\s+', ' ', cleaned_string)
        cleaned_string = cleaned_string.strip()
        if cleaned_string is not None:
            mj_wP+=1
        else:
            mj_woP+=1
    print("MJ image with prompt number: {}".format(mj_wP))
    print("MJ image without prompt number: {}".format(mj_woP))

    # Stable db
    file_path = 'processeddata/sd.json'
    sd_wP,sd_woP = 0,0
    dataset = json.load(open(file_path, "r"))
    for key,value in dataset.items():
        text = value['p']
        if text is not None:
            sd_wP+=1
        else:
            sd_woP+=1
    print("sd image with prompt number: {}".format(sd_wP))
    print("sd image without prompt number: {}".format(sd_woP))

    # Stable finetune
    data_path = "processeddata/data3.json"
    sdft_wP_selected, sdft_wP_uns,sdft_woP = 0,0,0
    hash2name = {}
    with open('processeddata/trainhash.txt', 'r') as f:
        for line in f:
            parts = line.split()
            key = parts[0]
            values = parts[1]
            hash2name[key] = values
    with open(data_path) as f:
        data = json.load(f)
    for key, value in data.items():
        if 'Prompt' in value and value['Prompt'] is not None:
            if 'Model' in value and value['Model'] == 'NovelAI':
                sdft_wP_selected+=1
            elif 'Model hash' in value:
                if value['Model hash'] in hash2name:
                    sdft_wP_selected += 1
                else:
                    sdft_wP_uns+=1
            else:
                sdft_wP_uns += 1
        else:
            sdft_woP+=1
    print("sdft image with prompt select number: {}".format(sdft_wP_selected))
    print("sdft image with prompt notselect number: {}".format(sdft_wP_uns))
    print("sdft image without prompt number: {}".format(sdft_woP))


get_image_w_prompt()

# real image number: 62154
# dalle image with prompt number: 31315
# dalle image without prompt number: 1420
# MJ image with prompt number: 21858
# MJ image without prompt number: 0
# sd image with prompt number: 10000
# sd image without prompt number: 0
# sdft image with prompt select number: 49670
# sdft image with prompt notselect number: 71308
# sdft image without prompt number: 989


# 训练、测试划分

# 筛选后，有prompt的图片数量，和图片选择
def get_allselected_imagekey():
    all_keys = []
    files = os.listdir('datasets/dddb/0_real')
    for i, file_name in enumerate(files):
        image = 'real/' + file_name
        all_keys.append(image)
    # Dalle
    dalle_dataset = json.load(open("processeddata/dalle.json", "r"))
    for key,value in dalle_dataset.items():
        text = value['Prompt']
        if text is not None:
            image_id = key.split('\\')[-1]
            image_path = '{}/{}'.format('dalle', image_id)
            all_keys.append(image_path)

    # Midjourney
    data = json.load(open("processeddata/mj_up.json", "r"))
    root_dir = "datasets/mj/downloads"
    files = os.listdir(root_dir)
    for i, file_name in enumerate(files):
        key = 'mj/' + file_name
        values = data[key]
        input_string = values["Prompt"]
        cleaned_string = re.sub(r'<[^>]+>', '', input_string)
        cleaned_string = re.sub(r'\s*--[^\s\d]+(?:\s+\d+:\d+)*', '', cleaned_string)
        cleaned_string = re.sub(r'\s+', ' ', cleaned_string)
        cleaned_string = cleaned_string.strip()
        if cleaned_string is not None:
            all_keys.append(key)

    # Stable db
    file_path = 'processeddata/sd.json'
    dataset = json.load(open(file_path, "r"))
    for key,value in dataset.items():
        text = value['p']
        if text is not None:
            image_id = key
            image_path = '{}/{}'.format('sd', image_id)
            all_keys.append(image_path)

    # Stable finetune
    data_path = "processeddata/data3.json"
    hash2name = {}
    with open('processeddata/trainhash.txt', 'r') as f:
        for line in f:
            parts = line.split()
            key = parts[0]
            values = parts[1]
            hash2name[key] = values
    with open(data_path) as f:
        data = json.load(f)
    for key, value in data.items():
        if 'Prompt' in value and value['Prompt'] is not None:
            if 'Model' in value and value['Model'] == 'NovelAI':
                image_id = key.split('\\')[-1]
                image_path = '{}/{}'.format('sdft', image_id)
                all_keys.append(image_path)

            elif 'Model hash' in value:
                if value['Model hash'] in hash2name:
                    image_id = key.split('\\')[-1]
                    image_path = '{}/{}'.format('sdft', image_id)
                    all_keys.append(image_path)
    return all_keys

all_keys = get_allselected_imagekey()
# 174997 images


selected_keys = []
train = json.load(open("processeddata/all_train.json", "r"))
for ii in train:
    selected_keys.append(ii['image'])


unselected_images = []
for ii in all_keys:
    print(ii)
    if ii not in selected_keys:
        unselected_images.append(ii)


# deepfake detection/copyright dataset

# 选1w张real作为测试，其余数据集都2500张
real_test = []
feke_sdft_test = []
feke_sd_test = []
feke_dalle_test = []
feke_mj_test = []
for item in unselected_images:
    typename = item.split('/')[0]
    if typename == 'real':
        real_test.append(item)
    elif typename == 'sdft':
        feke_sdft_test.append(item)
    elif typename == 'sd':
        feke_sd_test.append(item)
    elif typename == 'dalle':
        feke_dalle_test.append(item)
    elif typename == 'mj':
        feke_mj_test.append(item)


with open('./testset.txt', 'w', encoding='utf-8') as f:
    for item in real_test[:10000]:
        line = "{}\t{}\n".format(item, 0)
        f.write(line)
    for item in feke_sdft_test[:2500]:
        line = "{}\t{}\n".format(item, 1)
        f.write(line)
    for item in feke_dalle_test[:2500]:
        line = "{}\t{}\n".format(item, 1)
        f.write(line)
    for item in feke_mj_test[:2500]:
        line = "{}\t{}\n".format(item, 1)
        f.write(line)
    for item in feke_sd_test[:2500]:
        line = "{}\t{}\n".format(item, 1)
        f.write(line)

test_set = {}
with open('testset.txt', 'r') as f:
    for line in f:
        parts = line.split()
        key = parts[0]
        values = parts[1]
        test_set[key] = values


#######################################

def get_all_dalle_prompts():
    p = []
    dalle_dataset = json.load(open("processeddata/dalle.json", "r"))
    for key,value in dalle_dataset.items():
        text = value['Prompt']
        if text is not None:
            p.append(text)
    return p


def get_all_sdft_prompts():
    p = []
    data_path = "processeddata/data3.json"
    hash2name = {}
    with open('processeddata/trainhash.txt', 'r') as f:
        for line in f:
            parts = line.split()
            key = parts[0]
            values = parts[1]
            hash2name[key] = values
    with open(data_path) as f:
        data = json.load(f)
    for key, value in data.items():
        if 'Prompt' in value and value['Prompt'] is not None:
            if 'Model' in value and value['Model'] == 'NovelAI':
                text = value['Prompt']
                clean_text = re.sub(r'[\[\](\n<>\.{} ]+|lora:.+?(?=\s*,|\s*$)+|\d+\)+|\)+|:\d', '', text).strip()
                clean_text = re.sub(r',+', ',', clean_text).strip().lstrip(", ")
                p.append(clean_text)

            elif 'Model hash' in value:
                if value['Model hash'] in hash2name:
                    text = value['Prompt']
                    clean_text = re.sub(r'[\[\](\n<>\.{} ]+|lora:.+?(?=\s*,|\s*$)+|\d+\)+|\)+|:\d', '', text).strip()
                    clean_text = re.sub(r',+', ',', clean_text).strip().lstrip(", ")
                    p.append(clean_text)
    return p

def get_all_sdft_negativeprompts():
    p = []
    data_path = "processeddata/data3.json"
    with open(data_path) as f:
        data = json.load(f)
    for key, value in data.items():
        if 'Negative prompt' in value and value['Negative prompt'] is not None:
            text = value['Negative prompt']
            clean_text = re.sub(r'[\[\](\n<>\.{} ]+|lora:.+?(?=\s*,|\s*$)+|\d+\)+|\)+|:\d', '', text).strip()
            clean_text = re.sub(r',+', ',', clean_text).strip().lstrip(", ")
            p.append(clean_text)
    return p


def get_all_sd_prompts():
    p = []
    file_path = 'processeddata/sd.json'
    dataset = json.load(open(file_path, "r"))
    for key,value in dataset.items():
        text = value['p']
        if text is not None:
            p.append(text)
    return p

def get_all_mj_prompts():
    p = []
    data = json.load(open("processeddata/mj_up.json", "r"))
    root_dir = "rawimages/mj"
    files = os.listdir(root_dir)
    for i, file_name in enumerate(files):
        key = 'mj/' + file_name
        values = data[key]
        input_string = values["Prompt"]
        cleaned_string = re.sub(r'<[^>]+>', '', input_string)
        if "--" in cleaned_string:
            index = cleaned_string.index("--")
            cleaned_string = cleaned_string[:index]
        # cleaned_string = re.sub(r'\s+', ' ', cleaned_string)
        # cleaned_string = cleaned_string.strip()
        if cleaned_string is not None:
            p.append(cleaned_string)
    return p


from wordcloud import WordCloud, STOPWORDS
stopwords = set(STOPWORDS)

def show_wordcloud(data, name):
    wordcloud = WordCloud(
        background_color='white',
        stopwords=stopwords,
        max_words=200,
        max_font_size=80,
        scale=5,
        width=1000, height=512,
        repeat=False,
        random_state=1  # chosen at random by flipping a coin; it was heads
    ).generate(str(data))
    plt.figure(dpi=300)
    plt.axis('off')
    plt.imshow(wordcloud)
    plt.savefig(name, bbox_inches="tight")


show_wordcloud(get_all_dalle_prompts(), 'dalle.png')
show_wordcloud(get_all_sdft_prompts(), 'sdft.png')
show_wordcloud(get_all_sd_prompts(), 'sd.png')
show_wordcloud(get_all_mj_prompts(), 'mj.png')
show_wordcloud(get_all_sdft_negativeprompts(), 'sdft_nega.png')


def prompt_piechart(prompts, output):
    words = WordCloud(
        background_color='white',
        stopwords=stopwords,
        max_words=200,
        max_font_size=80,
        scale=5,
        width=1000, height=512,
        repeat=False,
        random_state=1  # chosen at random by flipping a coin; it was heads
    ).process_text(str(prompts))
    sorted_dict = dict(sorted(words.items(), key=lambda x: x[1], reverse=True))
    top_20 = dict(list(sorted_dict.items())[:20])
    x = np.char.array(list(top_20.keys()))
    y = np.array(list(top_20.values()))
    porcent = 100.*y/y.sum()
    new_colors = list(plt.cm.tab20c.colors)
    patches, texts = plt.pie(y, startangle=90, colors=new_colors)
    plt.show()
    plt.pie(y, startangle=90, autopct='%1.1f%%', colors=new_colors)
    labels = ['{0} - {1:1.1f} %'.format(i,j) for i,j in zip(x, porcent)]

    sort_legend = True
    if sort_legend:
        patches, labels, dummy = zip(*sorted(zip(patches, labels, y),key=lambda x: x[2],reverse=True))

    plt.legend(patches, labels, loc='center left', bbox_to_anchor=(0.9, 0.5),fontsize=8)
    # plt.title('Top 20 Negative Prompt Words by Frequency')
    plt.savefig(output, bbox_inches="tight")


prompt_piechart(get_all_dalle_prompts(), 'top20_dalle.pdf')
prompt_piechart(get_all_sdft_prompts(), 'top20_sdft.pdf')
prompt_piechart(get_all_sd_prompts(), 'top20_sd.pdf')
prompt_piechart(get_all_mj_prompts(), 'top20_mj.pdf')
prompt_piechart(get_all_sdft_negativeprompts(), 'top20_sdftng.pdf')



p = []
data_path = "processeddata/data3.json"
with open(data_path) as f:
    data = json.load(f)
for key, value in data.items():
    if 'Sampler' in value and value['Sampler'] is not None:
        text = value['Sampler']
        p.append(text)
        # p.append(float(text))

words = {x: p.count(x) for x in set(p)}
sorted_dict = dict(sorted(words.items(), key=lambda x: x[1], reverse=True))
top_20 = dict(list(sorted_dict.items())[:20])
x = np.array(list(top_20.keys()))
y = np.array(list(top_20.values()))
porcent = 100. * y / y.sum()
new_colors = list(plt.cm.tab20c.colors)
patches, texts = plt.pie(y, startangle=90, colors=new_colors)
plt.show()
autopct = lambda v: f'{v:1.1f}%' if v > 3 else None
plt.pie(y, startangle=90, autopct=autopct, colors=new_colors)
# plt.pie(y, startangle=90, autopct='%1.1f%%', colors=new_colors)
labels = ['{0} - {1:1.1f} %'.format(i, j) for i, j in zip(x, porcent)]

sort_legend = True
if sort_legend:
    patches, labels, dummy = zip(*sorted(zip(patches, labels, y), key=lambda x: x[2], reverse=True))

plt.legend(patches, labels, loc='center left', bbox_to_anchor=(0.9, 0.5), fontsize=8)
# plt.show()
plt.savefig('Sampler.pdf', bbox_inches="tight")


# Steps
# Sampler
# CFG scale


# promps长度
import seaborn as sns
sns.set(font="Times New Roman")
max_length = 150

# MidJourney truncates the input prompts at ~60 tokens.
sdft_prompts = get_all_sdft_prompts()
sdft_lengths = []
for r in sdft_prompts:
    if len(r.split(" "))< max_length:
        sdft_lengths.append(len(r.split(" ")))

mj_prompts = get_all_mj_prompts()
mj_lengths = []
for r in mj_prompts:
    if len(r.split(" "))< max_length:
        mj_lengths.append(len(r.split(" ")))

sd_prompts = get_all_sd_prompts()
sd_lengths = []
for r in sd_prompts:
    if len(r.split(" "))< max_length:
        sd_lengths.append(len(r.split(" ")))

dalle_prompts = get_all_dalle_prompts()
dalle_lengths = []
for r in dalle_prompts:
    if len(r.split(" "))< max_length:
        dalle_lengths.append(len(r.split(" ")))


fig, ax = plt.subplots()
plt.xlim(0,max_length)
sns.histplot(dalle_lengths, stat='percent', binwidth=5, kde=False, element="step", fill=False, label='DALL·E')
sns.histplot(sdft_lengths, stat='percent', binwidth=5, kde=False, element="step", fill=False, label='Personalized Diffusions')
sns.histplot(sd_lengths, stat='percent', binwidth=5, kde=False, element="step", fill=False, label='Stable Diffusion')
sns.histplot(mj_lengths, stat='percent', binwidth=5, kde=False, element="step", fill=False, label='MidJourney')
ax.legend()
ax.set(xlabel='Prompt Lengths', ylabel='Probability (%)')
plt.savefig('promptlength.pdf', bbox_inches="tight")





# Models
hash2num_s = {}
with open('processeddata/hash2num_supermodel.txt', 'r') as f:
    for line in f:
        parts = line.strip().split(' ')
        key = parts[0]
        values = parts[1]
        hash2num_s[key] = values

import numpy as np
from matplotlib import cm

hashsearch = np.load('datasets/civitai/hashsearch.npy',allow_pickle=True).item()

alllines = {}
with open('./processeddata/hash2num_superall.txt', 'r') as f:
    for line in f:
        parts = line.strip().split(' ')
        key = parts[0]
        values = parts[1]
        if len(hashsearch[key].split('\t')) > 1:
            name, id, mid, url = hashsearch[key].split('\t')
            if name not in alllines:
                alllines[name] = int(values)
        else:
            alllines[key] = int(values)

sorted_items = sorted(alllines.items(), key=lambda x: x[1], reverse=True)

topk=20
allnum, selectednum  = 0,0
selected = []
selected_num = []
for id, (key, value) in enumerate(sorted_items):
    if id < topk:
        allnum +=value
        selectednum +=value
        selected.append(key)
        selected_num.append(value)
    else:
        allnum +=value

selected[6] = 'AbyssOrangeMix2'
selected[18] = 'Anything V5'
selected[13] = 'YesMix'
selected[11] = 'Perfect World'
selected[19] = 'GuoFeng3'
selected.append('others')
selected_num.append(allnum - selectednum)

new_colors = list(plt.cm.tab20c.colors)
new_colors.append(new_colors[-1])
plt.gca().axis("equal")
autopct = lambda v: f'{v:1.1f}%' if v > 2 else None
pie = plt.pie(selected_num, startangle=0, autopct=autopct, pctdistance=0.9, radius=1.2, colors=new_colors)
porcent = 100. * np.array(selected_num) / np.array(selected_num).sum()
labels = ['{0} - {1:1.1f} %'.format(i, j) for i, j in zip(selected, porcent)]
# plt.title('Top 20 Models', weight='bold', size=14)
plt.legend(pie[0],labels, bbox_to_anchor=(1,0.5), loc="center right", fontsize=10,
           bbox_transform=plt.gcf().transFigure)
plt.subplots_adjust(left=0.0, bottom=0.1, right=0.6)
# plt.show()
plt.savefig('topmodels.pdf', bbox_inches="tight")







# 所有模型数量
# num_models = 3434
# 总共选的有模型的数量：70929
# 前20模型图片数量： 29516






