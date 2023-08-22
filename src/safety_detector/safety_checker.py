import os
from PIL import Image
import numpy as np
import json
from tqdm import tqdm

import onnx
import onnxruntime

import torch
from torchvision import datasets, transforms
from torch.utils.data import Dataset
from torch.utils.data import DataLoader

DEVICE_NAME = 'cuda' if torch.cuda.is_available() else 'cpu'
DEVICE_INDEX = 2     # Replace this with the index of the device you want to run on
DEVICE=f'{DEVICE_NAME}:{DEVICE_INDEX}'

work_id = 3


def create_session(model: str) -> onnxruntime.InferenceSession:
    providers = ['CPUExecutionProvider']
    if torch.cuda.is_available():
        providers.insert(DEVICE_INDEX, 'CUDAExecutionProvider')
    return onnxruntime.InferenceSession(model, providers=providers)

class CustomImageDataset(Dataset):
    def __init__(self, dataset_dir, json_file, transform=None):
        super().__init__()
        self.directory = dataset_dir

        # json_file = r'D:\workspace\hug\storage\pd.json'
        with open(json_file, 'r') as file:
            json_data = json.load(file)

        self.transform = transform
        # only check existing images
        self.image_files = [key for key in json_data.keys() if os.path.exists(os.path.join(self.directory, key))]

        self.prompts = []
        for i in self.image_files:
            if 'Prompt' in json_data[i]:
                self.prompts.append(json_data[i]['Prompt'])
            else:
                self.prompts.append('')

    def __len__(self):
        return len(self.image_files)

    def __getitem__(self, idx):
        image_path = os.path.join(self.directory, self.image_files[idx])
        image = Image.open(image_path).convert('RGB')  # convert image to RGB
        if self.transform:
            image = self.transform(image)
        prompt = self.prompts[idx]
        return self.image_files[idx], image, prompt

class ImageDirDataset(Dataset):
    def __init__(self, dataset_dir, transform=None):
        super().__init__()
        self.directory = dataset_dir
        all_files = os.listdir(self.directory)
        self.image_files = [f for f in all_files if any(f.endswith(ext) for ext in ['.jpg', '.png', '.jpeg'])]
        self.prompts = ['' for _ in self.image_files]
        self.transform = transform

    def __len__(self):
        return len(self.image_files)

    def __getitem__(self, idx):
        image_path = os.path.join(self.directory, self.image_files[idx])
        image = Image.open(image_path).convert('RGB')  # convert image to RGB
        if self.transform:
            image = self.transform(image)
        prompt = self.prompts[idx]
        return self.image_files[idx], image, prompt

def create_dataloader(dirpath, jsonfile, output_size=(260, 260)):
    transform = transforms.Compose([
        transforms.Resize(output_size),  # resize to the specified output size
        transforms.ToTensor(),  # transform the image to a tensor
        transforms.Lambda(lambda x: x.permute((1, 2, 0)))
    ])
    # Create an instance of the dataset
    if jsonfile is not None:
        dataset = CustomImageDataset(dirpath, jsonfile, transform=transform)
    else:
        dataset = ImageDirDataset(dirpath, transform=transform)
    # Set the parameters
    batch_size = 64
    num_workers = 8
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=False, num_workers=num_workers)
    return dataloader

def laion_safety_detector(model_path, dirpath, jsonfile):
    # onnx_model = onnx.load(model_path)
    # onnx.checker.check_model(onnx_model)
    dataloader = create_dataloader(dirpath, jsonfile, output_size=(260, 260))
    session = create_session(model_path)
    binding = session.io_binding()

    nsfw_results = {}
    for ids, images, prompts in tqdm(dataloader):
        x_tensor = images.to(DEVICE)
        binding.bind_input(
            name='input_1',
            device_type=DEVICE_NAME,
            device_id=DEVICE_INDEX,
            element_type=np.float32,
            shape=tuple(x_tensor.shape),
            buffer_ptr=x_tensor.data_ptr(),
        )
        z_tensor = torch.empty([x_tensor.shape[0],5], dtype=torch.float32, device=DEVICE)
        binding.bind_output(
            name='dense',
            device_type=DEVICE_NAME,
            device_id=DEVICE_INDEX,
            element_type=np.float32,
            shape=tuple(z_tensor.shape),
            buffer_ptr=z_tensor.data_ptr(),
        )
        session.run_with_iobinding(binding)

        output = torch.softmax(z_tensor, dim=1).cpu().numpy()
        trans_mat = np.array([[0.0, 1.0, 0.0, 1.0, 1.0, ]]).transpose()
        nsfw_scores_binary = np.dot(output, trans_mat).reshape(-1)
        #print(nsfw_scores_binary)
        for ii in range(x_tensor.shape[0]):
            nsfw_results[ids[ii]]={'nsfw_score_binary': nsfw_scores_binary[ii],
                                   'nsfw_score':output[ii].tolist()}
        # import pdb;pdb.set_trace()
    return nsfw_results

def gantman_nsfw_detector(model_path, dirpath, jsonfile):
    # onnx_model = onnx.load(model_path)
    # onnx.checker.check_model(onnx_model)
    dataloader = create_dataloader(dirpath, jsonfile, output_size=(224, 224))
    session = create_session(model_path)
    binding = session.io_binding()
    nsfw_results = {}
    for ids, images, prompts in tqdm(dataloader):
        x_tensor = images.to(DEVICE)

        binding.bind_input(
            name='keras_layer_input',
            device_type=DEVICE_NAME,
            device_id=DEVICE_INDEX,
            element_type=np.float32,
            shape=tuple(x_tensor.shape),
            buffer_ptr=x_tensor.data_ptr(),
        )

        z_tensor = torch.empty([x_tensor.shape[0], 5], dtype=torch.float32, device=DEVICE)
        binding.bind_output(
            name='prediction',
            device_type=DEVICE_NAME,
            device_id=DEVICE_INDEX,
            element_type=np.float32,
            shape=tuple(z_tensor.shape),
            buffer_ptr=z_tensor.data_ptr(),
        )

        session.run_with_iobinding(binding)
        output = torch.softmax(z_tensor, dim=1).cpu().numpy()
        trans_mat = np.array([[0.0, 1.0, 0.0, 1.0, 1.0, ]]).transpose()
        nsfw_scores_binary = np.dot(output, trans_mat).reshape(-1)
        #print(nsfw_scores_binary)
        for ii in range(x_tensor.shape[0]):
            nsfw_results[ids[ii]]={'nsfw_score_binary': nsfw_scores_binary[ii],
                                   'nsfw_score':output[ii].tolist()}
    return nsfw_results

def laion_CLIP_based_NSFW_Detector(model_path, dirpath, jsonfile):
    import clip

    def normalized(a, axis=-1, order=2):
        l2 = torch.norm(a, p=order, dim=axis, keepdim=True)
        l2[l2 == 0] = 1
        return a / l2

    model, preprocess = clip.load("ViT-L/14", device=DEVICE)
    if jsonfile is not None:
        dataset = CustomImageDataset(dirpath, jsonfile, transform=preprocess)
    else:
        dataset = ImageDirDataset(dirpath, transform=preprocess)
    batch_size = 64
    num_workers = 8
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=False, num_workers=num_workers)
    session = create_session(model_path)
    binding = session.io_binding()

    nsfw_results = {}
    for ids, images, prompts in tqdm(dataloader):
        images = images.to(DEVICE)
        with torch.no_grad():
            image_features = model.encode_image(images)
        x_tensor = normalized(image_features).double()
        binding.bind_input(
            name='input_1',
            device_type=DEVICE_NAME,
            device_id=DEVICE_INDEX,
            element_type=np.float64,
            shape=tuple(x_tensor.shape),
            buffer_ptr=x_tensor.data_ptr(),
        )

        z_tensor = torch.empty([x_tensor.shape[0], 1], dtype=torch.float32, device=DEVICE)
        binding.bind_output(
            name='classification_head_1',
            device_type=DEVICE_NAME,
            device_id=DEVICE_INDEX,
            element_type=np.float32,
            shape=tuple(z_tensor.shape),
            buffer_ptr=z_tensor.data_ptr(),
        )
        session.run_with_iobinding(binding)
        #print(z_tensor.item())
        for ii in range(x_tensor.shape[0]):
            nsfw_results[ids[ii]]={'nsfw_score':z_tensor[ii].item()}

    return nsfw_results

def sd_safety_checker(dirpath, jsonfile):
    from diffusers.pipelines.stable_diffusion.safety_checker import StableDiffusionSafetyChecker
    from transformers import AutoFeatureExtractor
    safety_checker = StableDiffusionSafetyChecker.from_pretrained(
        "CompVis/stable-diffusion-safety-checker", local_files_only=False)
    feature_extractor = AutoFeatureExtractor.from_pretrained(
        "CompVis/stable-diffusion-safety-checker", local_files_only=False
    )
    safety_checker.to(DEVICE)
    preprocess = transforms.Compose([
        transforms.Resize([224,224]),  # resize to the specified output size
        transforms.ToTensor(),  # transform the image to a tensor
    ])
    if jsonfile is not None:
        dataset = CustomImageDataset(dirpath, jsonfile, transform=preprocess)
    else:
        dataset = ImageDirDataset(dirpath, transform=preprocess)
    batch_size = 64
    num_workers = 8
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=False, num_workers=num_workers)

    nsfw_results = {}
    for ids, images, prompts in tqdm(dataloader):
        images = images.to(DEVICE)
        image_arrays = [images[x] for x in range(images.shape[0])]
        safety_checker_input = feature_extractor(image_arrays, return_tensors="pt").to(DEVICE)
        image, nsfw_detected = safety_checker(images=images.to(DEVICE),clip_input=safety_checker_input.pixel_values.to(DEVICE))
        #print(nsfw_detected)
        for ii in range(images.shape[0]):
            nsfw_results[ids[ii]]={'nsfw_result':nsfw_detected[ii]}
    return nsfw_results

if __name__ == "__main__":

    if work_id == 0:
        sd_safety_results = sd_safety_checker(dirpath="/home/teddy/workspace/datasets/aiart/sdft",
                                              jsonfile="/home/teddy/workspace/datasets/aiart/pd.json")
        with open('sd_safety_results.json', 'w') as json_file:
            json.dump(sd_safety_results, json_file, indent=4)
    elif work_id == 1:
        laion_CLIP_based_NSFW_results = laion_CLIP_based_NSFW_Detector(model_path="./clip_nsfw_l14.onnx",
                                                           dirpath="/home/teddy/workspace/datasets/aiart/sdft",
                                                           jsonfile="/home/teddy/workspace/datasets/aiart/pd.json")
        with open('laion_CLIP_based_NSFW_results.json', 'w') as json_file:
            json.dump(laion_CLIP_based_NSFW_results, json_file, indent=4)

    elif work_id == 2:
        laion_safety_results = laion_safety_detector(model_path="./laion_nsfw.onnx",
                                                  dirpath="/home/teddy/workspace/datasets/aiart/sdft",
                                                  jsonfile="/home/teddy/workspace/datasets/aiart/pd.json")
        with open('laion_safety_results.json', 'w') as json_file:
            json.dump(laion_safety_results, json_file, indent=4)

    elif work_id == 3:
        gantman_nsfw_results = gantman_nsfw_detector(model_path="./gantman_nsfw.onnx",
                                                  dirpath="/home/teddy/workspace/datasets/aiart/sdft",
                                                  jsonfile="/home/teddy/workspace/datasets/aiart/pd.json")
        with open('gantman_nsfw_results.json', 'w') as json_file:
            json.dump(gantman_nsfw_results, json_file, indent=4)



    if work_id == 0:
        sd_safety_results = sd_safety_checker(dirpath="/home/teddy/workspace/datasets/aiart/sd",
                                              jsonfile="/home/teddy/workspace/datasets/aiart/sd.json")
        with open('sd_safety_sd.json', 'w') as json_file:
            json.dump(sd_safety_results, json_file, indent=4)
    elif work_id == 1:
        laion_CLIP_based_NSFW_results = laion_CLIP_based_NSFW_Detector(model_path="./clip_nsfw_l14.onnx",
                                                           dirpath="/home/teddy/workspace/datasets/aiart/sd",
                                                           jsonfile="/home/teddy/workspace/datasets/aiart/sd.json")
        with open('laion_CLIP_based_NSFW_sd.json', 'w') as json_file:
            json.dump(laion_CLIP_based_NSFW_results, json_file, indent=4)

    elif work_id == 2:
        laion_safety_results = laion_safety_detector(model_path="./laion_nsfw.onnx",
                                                  dirpath="/home/teddy/workspace/datasets/aiart/sd",
                                                  jsonfile="/home/teddy/workspace/datasets/aiart/sd.json")
        with open('laion_safety_sd.json', 'w') as json_file:
            json.dump(laion_safety_results, json_file, indent=4)

    elif work_id == 3:
        gantman_nsfw_results = gantman_nsfw_detector(model_path="./gantman_nsfw.onnx",
                                                  dirpath="/home/teddy/workspace/datasets/aiart/sd",
                                                  jsonfile="/home/teddy/workspace/datasets/aiart/sd.json")
        with open('gantman_nsfw_sd.json', 'w') as json_file:
            json.dump(gantman_nsfw_results, json_file, indent=4)


    if work_id == 0:
        sd_safety_results = sd_safety_checker(dirpath="/home/teddy/workspace/datasets/aiart/mj",
                                              jsonfile="/home/teddy/workspace/datasets/aiart/mj.json")
        with open('sd_safety_mj.json', 'w') as json_file:
            json.dump(sd_safety_results, json_file, indent=4)
    elif work_id == 1:
        laion_CLIP_based_NSFW_results = laion_CLIP_based_NSFW_Detector(model_path="./clip_nsfw_l14.onnx",
                                                           dirpath="/home/teddy/workspace/datasets/aiart/mj",
                                                           jsonfile="/home/teddy/workspace/datasets/aiart/mj.json")
        with open('laion_CLIP_based_NSFW_mj.json', 'w') as json_file:
            json.dump(laion_CLIP_based_NSFW_results, json_file, indent=4)

    elif work_id == 2:
        laion_safety_results = laion_safety_detector(model_path="./laion_nsfw.onnx",
                                                  dirpath="/home/teddy/workspace/datasets/aiart/mj",
                                                  jsonfile="/home/teddy/workspace/datasets/aiart/mj.json")
        with open('laion_safety_mj.json', 'w') as json_file:
            json.dump(laion_safety_results, json_file, indent=4)

    elif work_id == 3:
        gantman_nsfw_results = gantman_nsfw_detector(model_path="./gantman_nsfw.onnx",
                                                  dirpath="/home/teddy/workspace/datasets/aiart/mj",
                                                  jsonfile="/home/teddy/workspace/datasets/aiart/mj.json")
        with open('gantman_nsfw_mj.json', 'w') as json_file:
            json.dump(gantman_nsfw_results, json_file, indent=4)



    if work_id == 0:
        sd_safety_results = sd_safety_checker(dirpath="/home/teddy/workspace/datasets/aiart/mj",
                                              jsonfile="/home/teddy/workspace/datasets/aiart/mj.json")
        with open('sd_safety_mj.json', 'w') as json_file:
            json.dump(sd_safety_results, json_file, indent=4)
    elif work_id == 1:
        laion_CLIP_based_NSFW_results = laion_CLIP_based_NSFW_Detector(model_path="./clip_nsfw_l14.onnx",
                                                           dirpath="/home/teddy/workspace/datasets/aiart/mj",
                                                           jsonfile="/home/teddy/workspace/datasets/aiart/mj.json")
        with open('laion_CLIP_based_NSFW_mj.json', 'w') as json_file:
            json.dump(laion_CLIP_based_NSFW_results, json_file, indent=4)

    elif work_id == 2:
        laion_safety_results = laion_safety_detector(model_path="./laion_nsfw.onnx",
                                                  dirpath="/home/teddy/workspace/datasets/aiart/mj",
                                                  jsonfile="/home/teddy/workspace/datasets/aiart/mj.json")
        with open('laion_safety_mj.json', 'w') as json_file:
            json.dump(laion_safety_results, json_file, indent=4)

    elif work_id == 3:
        gantman_nsfw_results = gantman_nsfw_detector(model_path="./gantman_nsfw.onnx",
                                                  dirpath="/home/teddy/workspace/datasets/aiart/mj",
                                                  jsonfile="/home/teddy/workspace/datasets/aiart/mj.json")
        with open('gantman_nsfw_mj.json', 'w') as json_file:
            json.dump(gantman_nsfw_results, json_file, indent=4)


    if work_id == 0:
        sd_safety_results = sd_safety_checker(dirpath="/home/teddy/workspace/datasets/aiart/test/parti/1_fake",
                                              jsonfile=None)
        with open('sd_safety_parti.json', 'w') as json_file:
            json.dump(sd_safety_results, json_file, indent=4)
    elif work_id == 1:
        laion_CLIP_based_NSFW_results = laion_CLIP_based_NSFW_Detector(model_path="./clip_nsfw_l14.onnx",
                                                           dirpath="/home/teddy/workspace/datasets/aiart/test/parti/1_fake",
                                                           jsonfile=None)
        with open('laion_CLIP_based_NSFW_parti.json', 'w') as json_file:
            json.dump(laion_CLIP_based_NSFW_results, json_file, indent=4)

    elif work_id == 2:
        laion_safety_results = laion_safety_detector(model_path="./laion_nsfw.onnx",
                                                  dirpath="/home/teddy/workspace/datasets/aiart/test/parti/1_fake",
                                                  jsonfile=None)
        with open('laion_safety_parti.json', 'w') as json_file:
            json.dump(laion_safety_results, json_file, indent=4)

    elif work_id == 3:
        gantman_nsfw_results = gantman_nsfw_detector(model_path="./gantman_nsfw.onnx",
                                                  dirpath="/home/teddy/workspace/datasets/aiart/test/parti/1_fake",
                                                  jsonfile=None)
        with open('gantman_nsfw_parti.json', 'w') as json_file:
            json.dump(gantman_nsfw_results, json_file, indent=4)


    if work_id == 0:
        sd_safety_results = sd_safety_checker(dirpath="/home/teddy/workspace/datasets/aiart/test/imagen/1_fake",
                                              jsonfile=None)
        with open('sd_safety_imagen.json', 'w') as json_file:
            json.dump(sd_safety_results, json_file, indent=4)
    elif work_id == 1:
        laion_CLIP_based_NSFW_results = laion_CLIP_based_NSFW_Detector(model_path="./clip_nsfw_l14.onnx",
                                                           dirpath="/home/teddy/workspace/datasets/aiart/test/imagen/1_fake",
                                                           jsonfile=None)
        with open('laion_CLIP_based_NSFW_imagen.json', 'w') as json_file:
            json.dump(laion_CLIP_based_NSFW_results, json_file, indent=4)

    elif work_id == 2:
        laion_safety_results = laion_safety_detector(model_path="./laion_nsfw.onnx",
                                                  dirpath="/home/teddy/workspace/datasets/aiart/test/imagen/1_fake",
                                                  jsonfile=None)
        with open('laion_safety_imagen.json', 'w') as json_file:
            json.dump(laion_safety_results, json_file, indent=4)

    elif work_id == 3:
        gantman_nsfw_results = gantman_nsfw_detector(model_path="./gantman_nsfw.onnx",
                                                  dirpath="/home/teddy/workspace/datasets/aiart/test/imagen/1_fake",
                                                  jsonfile=None)
        with open('gantman_nsfw_imagen.json', 'w') as json_file:
            json.dump(gantman_nsfw_results, json_file, indent=4)



    if work_id == 0:
        sd_safety_results = sd_safety_checker(dirpath="/home/teddy/workspace/datasets/aiart/dalle/",
                                              jsonfile=None)
        with open('sd_safety_dalle.json', 'w') as json_file:
            json.dump(sd_safety_results, json_file, indent=4)
    elif work_id == 1:
        laion_CLIP_based_NSFW_results = laion_CLIP_based_NSFW_Detector(model_path="./clip_nsfw_l14.onnx",
                                                           dirpath="/home/teddy/workspace/datasets/aiart/dalle",
                                                           jsonfile=None)
        with open('laion_CLIP_based_NSFW_dalle.json', 'w') as json_file:
            json.dump(laion_CLIP_based_NSFW_results, json_file, indent=4)

    elif work_id == 2:
        laion_safety_results = laion_safety_detector(model_path="./laion_nsfw.onnx",
                                                  dirpath="/home/teddy/workspace/datasets/aiart/dalle",
                                                  jsonfile=None)
        with open('laion_safety_dalle.json', 'w') as json_file:
            json.dump(laion_safety_results, json_file, indent=4)

    elif work_id == 3:
        gantman_nsfw_results = gantman_nsfw_detector(model_path="./gantman_nsfw.onnx",
                                                  dirpath="/home/teddy/workspace/datasets/aiart/dalle",
                                                  jsonfile=None)
        with open('gantman_nsfw_dalle.json', 'w') as json_file:
            json.dump(gantman_nsfw_results, json_file, indent=4)