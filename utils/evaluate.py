# Implementaion of CLIPEvaluation mainly comes from
# https://github.com/whitetiger1002/Dreambooth_Diffusion/blob/bb7daceaa7f5cf90dedc03d8b0b16c9b62d1edee/evaluation/clip_eval.py
# https://github.com/richzhang/PerceptualSimilarity

import os
import re
import json
import clip
import lpips
import open_clip
import numpy as np
from sklearn.metrics import f1_score
import PIL
from PIL import Image
from urllib.request import urlretrieve  # pylint: disable=import-outside-toplevel

import torch
import torch.nn as nn
from torchvision import transforms
from torch.utils.data import Dataset
from torch.utils.data import DataLoader

from cleanfid import fid
import shutil
from os.path import expanduser  # pylint: disable=import-outside-toplevel

class CLIPEvaluator(object):
    def __init__(self, device, clip_model='ViT-B/32') -> None:
        self.device = device
        self.model, clip_preprocess = clip.load(clip_model, device=self.device)

        self.clip_preprocess = clip_preprocess

        self.preprocess = transforms.Compose([transforms.Normalize(mean=[-1.0, -1.0, -1.0], std=[2.0, 2.0, 2.0])] +  # Un-normalize from [-1.0, 1.0] (generator output) to [0, 1].
                                             clip_preprocess.transforms[:2] +  # to match CLIP input scale assumptions
                                             clip_preprocess.transforms[4:])  # + skip convert PIL to tensor

    def tokenize(self, strings: list):
        return clip.tokenize(strings).to(self.device)

    @torch.no_grad()
    def encode_text(self, tokens: list) -> torch.Tensor:
        return self.model.encode_text(tokens)

    @torch.no_grad()
    def encode_images(self, images: torch.Tensor) -> torch.Tensor:
        images = self.preprocess(images).to(self.device)
        return self.model.encode_image(images)

    def get_text_features(self, text: str, norm: bool = True) -> torch.Tensor:

        tokens = clip.tokenize(text).to(self.device)

        text_features = self.encode_text(tokens).detach()

        if norm:
            text_features /= text_features.norm(dim=-1, keepdim=True)

        return text_features

    def get_image_features(self, img: torch.Tensor, norm: bool = True) -> torch.Tensor:
        image_features = self.encode_images(img)

        if norm:
            image_features /= image_features.clone().norm(dim=-1, keepdim=True)

        return image_features

    def img_to_img_similarity(self, src_images, generated_images):
        src_img_features = self.get_image_features(src_images)
        gen_img_features = self.get_image_features(generated_images)

        return (src_img_features @ gen_img_features.T).mean()

    def txt_to_img_similarity(self, text, generated_images):
        text_features = self.get_text_features(text)
        gen_img_features = self.get_image_features(generated_images)

        return (text_features @ gen_img_features.T).mean()

class ImageDirEvaluator(CLIPEvaluator):
    def __init__(self, device, clip_model='ViT-B/32') -> None:
        super().__init__(device, clip_model)

    def evaluate(self, gen_samples, src_images, target_text):
        sim_samples_to_img = self.img_to_img_similarity(src_images, gen_samples)
        sim_samples_to_text = self.txt_to_img_similarity(target_text, gen_samples)

        return sim_samples_to_img, sim_samples_to_text

    def evaluate_image(self, gen_samples, src_images):
        sim_samples_to_img = self.img_to_img_similarity(src_images, gen_samples)
        return sim_samples_to_img

class ImageDataset(Dataset):
    def __init__(self, ref_dir, gen_dir):
        self.ref_images = []
        self.gen_images = []

        for sub_dir in os.listdir(gen_dir):
            gen_img_dir = os.path.join(gen_dir, sub_dir)
            ref_img_dir = os.path.join(ref_dir, sub_dir)

            gen_image_names = os.listdir(gen_img_dir)
            gen_image_paths = [os.path.join(gen_img_dir, file_path) for file_path in gen_image_names]
            self.gen_images.append(gen_image_paths)

            ref_image_names = os.listdir(ref_img_dir)
            ref_image_paths = [os.path.join(ref_img_dir, file_path) for file_path in ref_image_names]
            self.ref_images.append(ref_image_paths)

        self.image_size = 224
        self.interpolation = {"linear": PIL.Image.LINEAR,
                              "bilinear": PIL.Image.BILINEAR,
                              "bicubic": PIL.Image.BICUBIC,
                              "lanczos": PIL.Image.LANCZOS,
                              }["bicubic"]

    def __len__(self):
        return len(self.gen_images)

    def process_image(self, path_list):
        images = []
        for img_path in path_list:
            image = Image.open(img_path)
            if not image.mode == "RGB":
                image = image.convert("RGB")
            image = image.resize((self.image_size, self.image_size), resample=self.interpolation)
            image = np.array(image).astype(np.uint8)
            images.append((image / 127.5 - 1.0).astype(np.float32))
        retrun_images = [torch.from_numpy(img).permute(2, 0, 1) for img in images]
        retrun_images = torch.stack(retrun_images, dim=0)
        return retrun_images

    def __getitem__(self, index):
        ref = self.process_image(self.ref_images[index])
        gen = self.process_image(self.gen_images[index])
        return ref, gen


class Evaluation(object):
    def __init__(self, org_dir, gen_dir):
        device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
        self.clipEvaluator = ImageDirEvaluator(device)
        dataset = ImageDataset(org_dir, gen_dir)
        batch_size = 1
        self.dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
        self.loss_fn_alex = lpips.LPIPS(net='alex')

    def simple_eval(self):
        sim_img_matrix, d_matrix = [], []
        for i, (ref, gen) in enumerate(self.dataloader):
            sim_samples_to_img = self.clipEvaluator.evaluate_image(gen, ref)
            d = self.loss_fn_alex(ref, gen).mean()
            sim_img_matrix.append(round(sim_samples_to_img.item(), 4))
            d_matrix.append(round(d.item(), 4))
        print("------------------------")
        print("Image-alignment: {}".format(sim_img_matrix))
        print("D matrix: {}".format(d_matrix))
        return sim_img_matrix, d_matrix

# fid_score = fid.compute_fid(src_dir, src_dir, model_name="inception_v3")
# clipfid_score = fid.compute_fid(src_dir, org_dir, mode="clean", model_name="clip_vit_b_32")
# kid_score = fid.compute_kid(src_dir, org_dir)

def deepfake_eval(test_file, predict_file):
    test_set = {}
    with open(test_file, 'r') as f:
        for line in f:
            parts = line.split()
            test_set[parts[0]] = parts[1]

    task_set = {'sdft':0, 'sd':0, 'mj':0, 'imagen':0, 'dalle':0, 'parti':0,'sdftood':0}
    task_set_num = {'sdft':0.001, 'sd':0.001, 'mj':0.001, 'imagen':0.001, 'dalle':0.001, 'parti':0.001, 'sdftood':0.001}
    correct = 0
    with open(predict_file, 'r') as f:
        for line in f:
            parts = line.split('\t')
            task = parts[0].split('/')[0]
            task_set_num[task]+=1
            try:
                gt = int(test_set[parts[0]])
                pred = parts[1]
                if 1 == gt and "ai generated" in pred:
                    correct += 1
                    task_set[task]+=1
                elif 0 ==gt and "real" in pred:
                    correct += 1
                    task_set[task]+=1
            except:
                pass
    for key, value in task_set.items():
        print("{} {}".format(key, value/task_set_num[key]))
    print(correct/len(test_set))



def copyright_eval(predict_file, json_file):
    dataset = json.load(open(json_file, "r"))
    label= {'real':1, 'dalle':2, 'mj':3, 'sd': 4}
    sdfts = []
    sdftmodels = {}
    for item in dataset:
        sdftmodels[item['image']] = item['output'].split()[3]
        sdfts.append(item['output'].split()[3])

    sdfts = set(sdfts)
    startnum = 5
    for i in sdfts:
        label[i] = startnum
        startnum+=1

    predict_set = {}
    with open(predict_file, 'r') as f:
        for line in f:
            parts = line.split('\t')
            predict_set[parts[0]] = parts[1].strip()

    correct=0
    preds = []
    trues = []

    for key, pred in predict_set.items():
        print(pred)
        subsetname, realfake, filename = key.split('/')
        if realfake == '0_real':
            if pred == 'This is a real image.':
                correct+=1
                preds.append(label['real'])
                trues.append(label['real'])
            else:
                trues.append(label['real'])
                if pred == 'This is an ai generated image by StableDiffusion.':
                    preds.append(label['sd'])
                elif pred == 'This is an ai generated image by Midjourney.':
                    preds.append(label['mj'])
                elif pred == 'This is an ai generated image by DALLE.':
                    preds.append(label['dalle'])
                elif subsetname == 'sdft':
                    predmodel = pred.split()[-1][:-1]
                    try:
                        preds.append(label[predmodel])
                    except:
                        preds.append(label['sd'])
                else:
                    preds.append(label['sd'])
        else:
            if subsetname == 'sd' and pred == 'This is an ai generated image by StableDiffusion.':
                correct += 1
                preds.append(label['sd'])
                trues.append(label['sd'])
            elif subsetname == 'mj' and pred == 'This is an ai generated image by Midjourney.':
                correct += 1
                preds.append(label['mj'])
                trues.append(label['mj'])
            elif subsetname == 'dalle' and pred == 'This is an ai generated image by DALLE.':
                correct += 1
                preds.append(label['dalle'])
                trues.append(label['dalle'])
            elif subsetname == 'sdft':
                gtmodel = sdftmodels['{}/{}'.format(subsetname, filename)]
                predmodel = pred.split()[-1][:-1]
                if gtmodel == predmodel:
                    correct += 1
                    preds.append(label[predmodel])
                    trues.append(label[gtmodel])
                else:
                    try:
                        preds.append(label[predmodel])
                    except:
                        preds.append(label['sd'])
                    trues.append(label[gtmodel])
                    # print(predmodel)
            else:
                preds.append(label[subsetname])
                if subsetname == 'sd':
                    trues.append(label['sd'])
                elif subsetname == 'mj':
                    trues.append(label['mj'])
                elif subsetname == 'dalle':
                    trues.append(label['dalle'])
                else:
                    gtmodel = sdftmodels['{}/{}'.format(subsetname, filename)]
                    trues.append(label[gtmodel])

    # import pdb;pdb.s？et_trace()
    f1 = f1_score(trues, preds, average='macro')
    print(f1)
    print(correct/len(predict_set))




def get_aesthetic_model(clip_model="vit_l_14"):
    """load the aethetic model"""
    cache_folder = "./ckpt"
    path_to_model = "./ckpt/sa_0_4_" + clip_model + "_linear.pth"
    if not os.path.exists(path_to_model):
        os.makedirs(cache_folder, exist_ok=True)
        url_model = (
                "https://github.com/LAION-AI/aesthetic-predictor/blob/main/sa_0_4_" + clip_model + "_linear.pth?raw=true"
        )
        urlretrieve(url_model, path_to_model)
    if clip_model == "vit_l_14":
        m = nn.Linear(768, 1)
    elif clip_model == "vit_b_32":
        m = nn.Linear(512, 1)
    else:
        raise ValueError()
    s = torch.load(path_to_model)
    m.load_state_dict(s)
    m.eval()
    return m



class ImagePathDataset(Dataset):
    def __init__(self, gen_dir):
        self.gen_images = []
        for sub_dir in os.listdir(gen_dir):
            gen_img_dir = os.path.join(gen_dir, sub_dir)
            gen_image_names = os.listdir(gen_img_dir)
            gen_image_paths = [os.path.join(gen_img_dir, file_path) for file_path in gen_image_names]
            self.gen_images.extend(gen_image_paths)

    def __len__(self):
        return len(self.gen_images)

    def __getitem__(self, index):
        return self.gen_images[index]

class Evaluation_Asethetic(object):
    def __init__(self, org_dir, gen_dir):
        device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
        dataset = ImagePathDataset(gen_dir)
        batch_size = 1
        self.dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
        self.amodel = get_aesthetic_model(clip_model="vit_l_14")
        self.amodel.eval()
        self.model, _, self.preprocess = open_clip.create_model_and_transforms('ViT-L-14', pretrained='openai')

    def simple_eval(self):
        predictions = []
        for i, path in enumerate(self.dataloader):
            # import pdb;pdb.set_trace()
            image = self.preprocess(Image.open(path[0])).unsqueeze(0)
            with torch.no_grad():
                image_features = self.model.encode_image(image)
                image_features /= image_features.norm(dim=-1, keepdim=True)
                prediction = self.amodel(image_features)
                predictions.append(prediction.item())
        print(sum(predictions)/len(predictions))
        return predictions


if __name__ == '__main__':
    # obj = Evaluation("./ref", "./blip")
    # sim_img_matrix, d_matrix = obj.simple_eval()

    obj = Evaluation_Asethetic("./ref", "./blip")
    a = obj.simple_eval()


    import pdb;pdb.set_trace()


deepfake_eval('deepfake_test.txt', 'our_dfnew.txt')
deepfake_eval('deepfake_test.txt', 'our_dfoodnew.txt')

copyright_eval('our_dfnew.txt', 'sdft_test_100.json')




