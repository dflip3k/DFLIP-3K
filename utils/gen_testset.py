import os.path
import random
import shutil
import numpy as np
from PIL import Image
import json
import re



# 测试图
# 论文图



# 找到之前下载的全部real laion数据
origdir_real = r"rawimages/real"
all_train_real = []
for ii in os.listdir(origdir_real):
    all_train_real.append(ii.split('.')[0])

# 找到选中作为cvpr投稿的real，不要用这些，别重复选
alldir_real = r"E:\datasets\aiart\real"
all_real = []
for ii in os.listdir(alldir_real):
    all_real.append(ii)

random.shuffle(all_real)

# 从all trai real中重新选的数据
already_sample_externalreal = []

# 给parti建测试集
all = np.load(r"E:\datasets\aiart\raw\parti.npy", allow_pickle=True)
all = all.item()
alreadyselected = []
origdir_real = r"E:\datasets\aiart\raw\real"
origdir_fake = r"E:\datasets\aiart\raw\parti"
target = 'rawimages/test/parti'
for key, values in all.items():
    index = 0
    flag = 0
    while index<len(values) and values[index]['id'] not in alreadyselected:
        try:
            image = Image.open(os.path.join(origdir_real, str(values[index]['id'])+'.jpeg'))
            image.save(os.path.join(target, '0_real', str(values[index]['id'])+'.jpeg'))
            shutil.copy(os.path.join(origdir_fake, key),
                        os.path.join(target, '1_fake', key))
            alreadyselected.append(values[index]['id'])
            flag =1
            print("{} success index {}".format(key, index))
            break
        except:
            index += 1
    if flag == 0:
        for item in all_real:
            if item.split('.')[0] not in already_sample_externalreal and item.split('.')[0] not in all_train_real:
                try:
                    image = Image.open(os.path.join(alldir_real, item))
                    image.save(os.path.join(target, '0_real', item))
                    shutil.copy(os.path.join(origdir_fake, key),
                                os.path.join(target, '1_fake', key))
                    alreadyselected.append(item.split('.')[0])
                    already_sample_externalreal.append(item.split('.')[0])
                    break
                except:
                    print(item)
                    
# 给imagen建测试集
all = np.load(r"E:\datasets\aiart\raw\imagen.npy", allow_pickle=True)
all = all.item()
alreadyselected = []
origdir_real = r"E:\datasets\aiart\raw\real"
origdir_fake = r"E:\datasets\aiart\raw\imagen"
target = 'rawimages/test/imagen'
for key, values in all.items():
    index = 0
    flag = 0
    while index<len(values) and values[index]['id'] not in alreadyselected:
        try:
            image = Image.open(os.path.join(origdir_real, str(values[index]['id'])+'.jpeg'))
            image.save(os.path.join(target, '0_real', str(values[index]['id'])+'.jpeg'))
            shutil.copy(os.path.join(origdir_fake, key),
                        os.path.join(target, '1_fake', key))
            alreadyselected.append(values[index]['id'])
            flag =1
            print("{} success index {}".format(key, index))
            break
        except:
            index += 1

    if flag == 0:
        for item in all_real:
            if item.split('.')[0] not in already_sample_externalreal and item.split('.')[0] not in all_train_real:
                try:
                    image = Image.open(os.path.join(alldir_real, item))
                    image.save(os.path.join(target, '0_real', item))
                    shutil.copy(os.path.join(origdir_fake, key),
                                os.path.join(target, '1_fake', key))
                    alreadyselected.append(item.split('.')[0])
                    already_sample_externalreal.append(item.split('.')[0])
                    break
                except:
                    print(item)

# 给dalle建测试集
all = np.load(r"E:\datasets\aiart\raw\dalle.npy", allow_pickle=True)
all = all.item()
alreadyselected = []
origdir_real = r"E:\datasets\aiart\raw\real"
origdir_fake = r"E:\datasets\aiart\raw\dalle"
target = 'rawimages/test/dalle'
for key, values in all.items():
    index = 0
    flag = 0
    try:
        while index<len(values) and values[index]['id'] not in alreadyselected:
            try:
                image = Image.open(os.path.join(origdir_real, str(values[index]['id'])+'.jpeg'))
                image.save(os.path.join(target, '0_real', str(values[index]['id'])+'.jpeg'))
                shutil.copy(os.path.join(origdir_fake, key),
                            os.path.join(target, '1_fake', key))
                alreadyselected.append(values[index]['id'])
                flag =1
                print("{} success index {}".format(key, index))
                break
            except:
                index += 1

        if flag == 0:
            for item in all_real:
                if item.split('.')[0] not in already_sample_externalreal and item.split('.')[0] not in all_train_real:
                    try:
                        image = Image.open(os.path.join(alldir_real, item))
                        image.save(os.path.join(target, '0_real', item))
                        shutil.copy(os.path.join(origdir_fake, key),
                                    os.path.join(target, '1_fake', key))
                        alreadyselected.append(item.split('.')[0])
                        already_sample_externalreal.append(item.split('.')[0])
                        break
                    except:
                        print(item)
    except:
        print(values)

# 给mj建测试集
all = np.load(r"E:\datasets\aiart\raw\mj.npy", allow_pickle=True)
all = all.item()
alreadyselected = []
origdir_real = r"E:\datasets\aiart\raw\real"
origdir_fake = r"E:\datasets\aiart\raw\mj"
target = 'rawimages/test/mj'
for key, values in all.items():
    index = 0
    flag = 0
    while index<len(values) and values[index]['id'] not in alreadyselected:
        try:
            image = Image.open(os.path.join(origdir_real, str(values[index]['id'])+'.jpeg'))
            image.save(os.path.join(target, '0_real', str(values[index]['id'])+'.jpeg'))
            shutil.copy(os.path.join(origdir_fake, key),
                        os.path.join(target, '1_fake', key))
            alreadyselected.append(values[index]['id'])
            print("{} success index {}".format(key, index))
            flag =1
            break
        except:
            index += 1

    if flag == 0:
        for item in all_real:
            if item.split('.')[0] not in already_sample_externalreal and item.split('.')[0] not in all_train_real:
                try:
                    image = Image.open(os.path.join(alldir_real, item))
                    image.save(os.path.join(target, '0_real', item))
                    shutil.copy(os.path.join(origdir_fake, key),
                                os.path.join(target, '1_fake', key))
                    alreadyselected.append(item.split('.')[0])
                    already_sample_externalreal.append(item.split('.')[0])
                    break
                except:
                    print(item)

# 给sdft建测试集 随机选足够数量的realimage
sdft_dir = 'rawimages/test/sdft/1_fake'
target = 'rawimages/test/sdft'
for key in os.listdir(sdft_dir):
    for item in all_real:
        if item.split('.')[0] not in already_sample_externalreal and item.split('.')[0] not in all_train_real:
            try:
                image = Image.open(os.path.join(alldir_real, item))
                image.save(os.path.join(target, '0_real', item))
                already_sample_externalreal.append(item.split('.')[0])
                break
            except:
                already_sample_externalreal.append(item.split('.')[0])
                print(item)


# Dalle数量不太够，再选几十张图，找到新数据里还没拿来训练的dalle图片
def get_alls_imagekey():
    all_keys = []
    # Dalle
    dalle_dataset = json.load(open("processeddata/dalle.json", "r"))
    for key,value in dalle_dataset.items():
        text = value['Prompt']
        if text is not None:
            image_id = key.split('\\')[-1]
            image_path = '{}/{}'.format('dalle', image_id)
            all_keys.append(image_path)

    return all_keys

all_keys = get_alls_imagekey()

selected_keys = []
train = json.load(open("processeddata/all_train.json", "r"))
for ii in train:
    selected_keys.append(ii['image'])

unselected_images = []
for ii in all_keys:
    if ii not in selected_keys:
        unselected_images.append(ii)


wantnum =32

origdir_fake = "rawimages/dalle"
target = 'rawimages/test/dalle'
index = 0
for values in unselected_images:
    shutil.copy(os.path.join(origdir_fake, os.path.basename(values) ),
                os.path.join(target, '1_fake', os.path.basename(values)))
    index+=1
    if index == wantnum:
        break


# 把generate qa生成的数据，复制到测试集，一般不用
# train = json.load(open('sdft_test_100.json', "r"))
# for ii in train:
#     shutil.copy(os.path.join('rawimages', ii['image']),
#                 os.path.join(r'D:\workspace\AI_generated_DB\rawimages\test\sdft\1_fake', os.path.basename(ii['image']))
#                 )


# 下面是做 deepfake detection， multiclass 训练的数据格式脚本
# create binary for cnndet
def cnndet_train_format(sourcedir, targetdir, all_trainfile="processeddata/all_train.json"):
    train = json.load(open(all_trainfile, "r"))
    realnum=0
    fakenum=0
    for ii in train:
        if ii['output'] == 'This is a real image.':
            if not os.path.exists(os.path.join(targetdir, '0_real')):
                os.mkdir(os.path.join(targetdir, '0_real'))
            shutil.copy(os.path.join(sourcedir, ii['image']),
                os.path.join(targetdir, '0_real', str(realnum)+'.'+os.path.basename(ii['image']).split('.')[-1])
            )
            realnum+=1
        elif 'ai generated image' in ii['output']:
            if not os.path.exists(os.path.join(targetdir, '1_fake')):
                os.mkdir(os.path.join(targetdir, '1_fake'))
            shutil.copy(os.path.join(sourcedir, ii['image']),
                os.path.join(targetdir, '1_fake', str(fakenum)+'.'+os.path.basename(ii['image']).split('.')[-1])
            )
            fakenum+=1


cnndet_train_format(r'D:\workspace\AI_generated_DB\rawimages', r'D:\workspace\AI_generated_DB\rawimages\cnndet',
                    all_trainfile="processeddata/balance_train.json")




# create imagenet format, identification
def imagenet_format(sourcedir, targetdir, all_trainfile):
    train = json.load(open(all_trainfile, "r"))
    for ii in train:
        if ii['output'] == 'This is a real image.':
            if not os.path.exists(os.path.join(targetdir, 'real')):
                os.mkdir(os.path.join(targetdir, 'real'))
            shutil.copy(os.path.join(sourcedir, ii['image']),
                os.path.join(targetdir, 'real', os.path.basename(ii['image']))
            )
        elif "You can use this prompt" in ii['output'] and "DALLE" in ii['input']:
            modelname = "DALLE"
            if not os.path.exists(os.path.join(targetdir, modelname)):
                os.mkdir(os.path.join(targetdir, modelname))
            shutil.copy(os.path.join(sourcedir, ii['image']),
                os.path.join(targetdir, modelname, os.path.basename(ii['image']))
            )

        elif "You can use this prompt" in ii['output'] and "Midjourney" in ii['input']:
            modelname = "Midjourney"
            if not os.path.exists(os.path.join(targetdir, modelname)):
                os.mkdir(os.path.join(targetdir, modelname))
            shutil.copy(os.path.join(sourcedir, ii['image']),
                os.path.join(targetdir, modelname, os.path.basename(ii['image']))
            )
        elif "I suggest using" in ii['output']:
            modelname = ii['output'].split()[3]
            if not os.path.exists(os.path.join(targetdir, modelname)):
                os.mkdir(os.path.join(targetdir, modelname))
            shutil.copy(os.path.join(sourcedir, ii['image']),
                os.path.join(targetdir, modelname, os.path.basename(ii['image']))
            )

# 直接把训练所有图片拿来做copyright
imagenet_format(r'D:\workspace\AI_generated_DB\rawimages', r'D:\workspace\AI_generated_DB\rawimages\multitrain\train',
                    all_trainfile="processeddata/balance_train.json")



# 下面是做 deepfake detection， multiclass 测试的数据格式脚本
# 先把sdft的所有测试图片拿出来放在val文件夹里
target_testdir = r'D:\workspace\AI_generated_DB\rawimages\multitrain\test'
imagenet_format(r'D:\workspace\AI_generated_DB\rawimages', target_testdir,
                    all_trainfile="sdft_test_100.json")
# 然后把其他的测试图也拿出来
origin_testdir = "rawimages/test"

method='dalle'
for image in os.listdir(os.path.join(origin_testdir, method, '0_real')):
    if not os.path.exists(os.path.join(target_testdir, 'real')):
        os.mkdir(os.path.join(target_testdir, 'real'))
    shutil.copy(os.path.join(origin_testdir, method, '0_real', image),
                os.path.join(target_testdir, 'real', image))
for image in os.listdir(os.path.join(origin_testdir, method, '1_fake')):
    if not os.path.exists(os.path.join(target_testdir, 'DALLE')):
        os.mkdir(os.path.join(target_testdir, 'DALLE'))
    shutil.copy(os.path.join(origin_testdir, method, '1_fake', image),
                os.path.join(target_testdir, 'DALLE', image))
method = 'mj'
for image in os.listdir(os.path.join(origin_testdir, method, '0_real')):
    if not os.path.exists(os.path.join(target_testdir, 'real')):
        os.mkdir(os.path.join(target_testdir, 'real'))
    shutil.copy(os.path.join(origin_testdir, method, '0_real', image),
                os.path.join(target_testdir, 'real', image))
for image in os.listdir(os.path.join(origin_testdir, method, '1_fake')):
    if not os.path.exists(os.path.join(target_testdir, 'Midjourney')):
        os.mkdir(os.path.join(target_testdir, 'Midjourney'))
    shutil.copy(os.path.join(origin_testdir, method, '1_fake', image),
                os.path.join(target_testdir, 'Midjourney', image))
method = 'sd'
for image in os.listdir(os.path.join(origin_testdir, method, '0_real')):
    if not os.path.exists(os.path.join(target_testdir, 'real')):
        os.mkdir(os.path.join(target_testdir, 'real'))
    shutil.copy(os.path.join(origin_testdir, method, '0_real', image),
                os.path.join(target_testdir, 'real', image))
for image in os.listdir(os.path.join(origin_testdir, method, '1_fake')):
    if not os.path.exists(os.path.join(target_testdir, 'StableDiffusion')):
        os.mkdir(os.path.join(target_testdir, 'StableDiffusion'))
    shutil.copy(os.path.join(origin_testdir, method, '1_fake', image),
                os.path.join(target_testdir, 'StableDiffusion', image))



# 输入给otter进行测试的代码，就是将所有的文件直接输入到text文件中
origin_testdir = "rawimages/test"
wirte_lines = []
method='dalle'
for image in os.listdir(os.path.join(origin_testdir, method, '0_real')):
    wirte_lines.append("{}\t0\n".format(os.path.join(method, '0_real', image).replace('\\', '/')))
for image in os.listdir(os.path.join(origin_testdir, method, '1_fake')):
    wirte_lines.append("{}\t1\n".format(os.path.join(method, '1_fake', image).replace('\\', '/')))
method = 'mj'
for image in os.listdir(os.path.join(origin_testdir, method, '0_real')):
    wirte_lines.append("{}\t0\n".format(os.path.join(method, '0_real', image).replace('\\', '/')))
for image in os.listdir(os.path.join(origin_testdir, method, '1_fake')):
    wirte_lines.append("{}\t1\n".format(os.path.join(method, '1_fake', image).replace('\\', '/')))
method = 'sd'
for image in os.listdir(os.path.join(origin_testdir, method, '0_real')):
    wirte_lines.append("{}\t0\n".format(os.path.join(method, '0_real', image).replace('\\', '/')))
for image in os.listdir(os.path.join(origin_testdir, method, '1_fake')):
    wirte_lines.append("{}\t1\n".format(os.path.join(method, '1_fake', image).replace('\\', '/')))
method = 'sdft'
for image in os.listdir(os.path.join(origin_testdir, method, '0_real')):
    wirte_lines.append("{}\t0\n".format(os.path.join(method, '0_real', image).replace('\\', '/')))
for image in os.listdir(os.path.join(origin_testdir, method, '1_fake')):
    wirte_lines.append("{}\t1\n".format(os.path.join(method, '1_fake', image).replace('\\', '/')))
method = 'parti'
for image in os.listdir(os.path.join(origin_testdir, method, '0_real')):
    wirte_lines.append("{}\t0\n".format(os.path.join(method, '0_real', image).replace('\\', '/')))
for image in os.listdir(os.path.join(origin_testdir, method, '1_fake')):
    wirte_lines.append("{}\t1\n".format(os.path.join(method, '1_fake', image).replace('\\', '/')))
method = 'imagen'
for image in os.listdir(os.path.join(origin_testdir, method, '0_real')):
    wirte_lines.append("{}\t0\n".format(os.path.join(method, '0_real', image).replace('\\', '/')))
for image in os.listdir(os.path.join(origin_testdir, method, '1_fake')):
    wirte_lines.append("{}\t1\n".format(os.path.join(method, '1_fake', image).replace('\\', '/')))
method='sdftood'
for image in os.listdir(os.path.join(origin_testdir, method, '0_real')):
    wirte_lines.append("{}\t0\n".format(os.path.join(method, '0_real', image).replace('\\', '/')))
for image in os.listdir(os.path.join(origin_testdir, method, '1_fake')):
    wirte_lines.append("{}\t1\n".format(os.path.join(method, '1_fake', image).replace('\\', '/')))

with open('./deepfake_ood_test.txt', 'w', encoding='utf-8') as f:
    for line in wirte_lines:
        f.write(line)







# prompt generation testset
# 选出来一个类被200张
# real dalle mj sd sdft 共1000张
origin_testdir = "rawimages/test"
wirte_lines = []
realnum, dallenum, mjnum, sdnum, sdftnum = 0,0,0,0,0
method='dalle'
for image in os.listdir(os.path.join(origin_testdir, method, '0_real')):
    if realnum < 50:
        wirte_lines.append("{}\n".format(os.path.join(method, '0_real', image).replace('\\', '/')))
        realnum+=1
for image in os.listdir(os.path.join(origin_testdir, method, '1_fake')):
    if dallenum < 200:
        wirte_lines.append("{}\n".format(os.path.join(method, '1_fake', image).replace('\\', '/')))
        dallenum+=1
method = 'mj'
for image in os.listdir(os.path.join(origin_testdir, method, '0_real')):
    if realnum < 100:
        wirte_lines.append("{}\n".format(os.path.join(method, '0_real', image).replace('\\', '/')))
        realnum+=1
for image in os.listdir(os.path.join(origin_testdir, method, '1_fake')):
    if mjnum < 200:
        wirte_lines.append("{}\n".format(os.path.join(method, '1_fake', image).replace('\\', '/')))
        mjnum+=1
method = 'sd'
for image in os.listdir(os.path.join(origin_testdir, method, '0_real')):
    if realnum < 150:
        wirte_lines.append("{}\n".format(os.path.join(method, '0_real', image).replace('\\', '/')))
        realnum+=1
for image in os.listdir(os.path.join(origin_testdir, method, '1_fake')):
    if sdnum < 200:
        wirte_lines.append("{}\n".format(os.path.join(method, '1_fake', image).replace('\\', '/')))
        sdnum+=1
method = 'sdft'
for image in os.listdir(os.path.join(origin_testdir, method, '0_real')):
    if realnum < 200:
        wirte_lines.append("{}\n".format(os.path.join(method, '0_real', image).replace('\\', '/')))
        realnum+=1
for image in os.listdir(os.path.join(origin_testdir, method, '1_fake')):
    if sdftnum < 200:
        wirte_lines.append("{}\n".format(os.path.join(method, '1_fake', image).replace('\\', '/')))
        sdftnum+=1
with open('./prompts_1k.txt', 'w', encoding='utf-8') as f:
    for line in wirte_lines:
        f.write(line)



####################把这1k个copy到reference 目录下
files = []
with open('./prompts_1k.txt', 'r', encoding='utf-8') as f:
    for line in f:
        parts = line.strip()
        files.append(parts)

rootdir = 'rawimages/test'
outdir = r'D:\workspace\AI_generated_DB\experiments\ref'
index = 0
for refimage in files:
    # dirname = os.path.splitext(os.path.basename(refimage))[0]
    dirname = str(index)
    os.mkdir(os.path.join(outdir, str(dirname)))
    image = Image.open(os.path.join(rootdir, refimage))
    image.save(os.path.join(outdir, str(dirname), 'ref.png'))
    index+=1


# copy出来给blip打标用
index = 0
for refimage in files:
    image = Image.open(os.path.join(rootdir, refimage))
    image.save(os.path.join(r'D:\workspace\AI_generated_DB\experiments', 'blip', str(index)+'.png'))
    index+=1



allreal = list(os.listdir('rawimages/real'))


with open("processeddata/balance_train.json", "r") as f:
    dataset = json.load(f)

allreal = []
for ii in dataset:
    allreal.append(ii['image'].split('/')[1])

for i in os.listdir('rawimages/test/dalle/0_real'):
    if i in allreal:
        print(i)

for i in os.listdir('rawimages/test/sd/0_real'):
    if i in allreal:
        print(i)

for i in os.listdir('rawimages/test/imagen/0_real'):
    if i in allreal:
        print(i)

for i in os.listdir('rawimages/test/parti/0_real'):
    if i in allreal:
        print(i)

for i in os.listdir('rawimages/test/mj/0_real'):
    if i in allreal:
        print(i)

for i in os.listdir('rawimages/test/sdft/0_real'):
    if i in allreal:
        print(i)





# 生成ood sdft的数据
import os
import shutil
import json
idsdft = []

for i in os.listdir("/home/yabin/datasets/aiart/test/sdft/1_fake"):
    idsdft.append('sdft/{}'.format(i))

train = json.load(open("/home/yabin/datasets/aiart/all_train.json", "r", encoding='utf-8'))
for ii in train:
    idsdft.append(ii['image'])

for i in os.listdir("/home/yabin/datasets/aiart/sdft"):
    if 'sdft/{}'.format(i) not in idsdft:
        shutil.copy(os.path.join("/home/yabin/datasets/aiart/sdft", i),
                    os.path.join("/home/yabin/datasets/aiart/test/sdftood/1_fake", i))
























