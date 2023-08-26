import multiprocessing
import pandas as pd
import torch
import argparse
import cv2
import numpy as np
from PIL import Image
from tqdm import tqdm
from pathlib import Path
from torchvision import transforms as T
from typing import Union
import csv
from tqdm import tqdm
from functools import partial
from typing import List, Union

from easyface.attributes.models import *
from easyface.utils.visualize import show_image
from easyface.utils.io import WebcamStream, VideoReader, VideoWriter, FPS
from detect_align import FaceDetectAlign

class Inference:
    def __init__(self, model: str, checkpoint: str, det_model: str, det_checkpoint: str) -> None:
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.gender_labels = ['Male', 'Female']
        self.race_labels = ['White', 'Black', 'Latino Hispanic', 'East Asian', 'Southeast Asian', 'Indian', 'Middle Eastern']
        self.age_labels = ['0-2', '3-9', '10-19', '20-29', '30-39', '40-49', '50-59', '60-69', '70+']

        self.model = eval(model)(len(self.gender_labels) + len(self.race_labels) + len(self.age_labels))
        self.model.load_state_dict(torch.load(checkpoint, map_location='cpu'))
        self.model = self.model.to(self.device)
        self.model.eval()

        self.align = FaceDetectAlign(det_model, det_checkpoint)

        self.preprocess = T.Compose([
            T.Resize((224, 224)),
            T.Lambda(lambda x: x / 255),
            T.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
        ])

    def postprocess(self, preds: torch.Tensor):
        race_logits, gender_logits, age_logits = preds[:, :7].softmax(dim=1), preds[:, 7:9].softmax(dim=1), preds[:, 9:18].softmax(dim=1)
        race_preds = torch.argmax(race_logits, dim=1)
        gender_preds = torch.argmax(gender_logits, dim=1)
        age_preds = torch.argmax(age_logits, dim=1)
        return [self.race_labels[idx] for idx in race_preds], [self.gender_labels[idx] for idx in gender_preds], [self.age_labels[idx] for idx in age_preds]
        
    def __call__(self, img_path: Union[str, np.ndarray]):
        faces, dets, image = self.align.detect_and_align_faces(img_path, (112, 112))
        if faces is None:
            return None

        pfaces = self.preprocess(faces.permute(0, 3, 1, 2)).to(self.device)
        
        with torch.inference_mode():
            preds = self.model(pfaces).detach().cpu()
        races, genders, ages = self.postprocess(preds)

        results = []
        for race, gender, age in zip(races, genders, ages):
            results.append([img_path, race, gender, age])
        return results

def process_images(images: List[str], args: dict):
    inference = Inference(**args)
    results = []
    for img_path in images:
        file_path = Path(img_path)
        if file_path.is_file():
            result = inference(str(file_path))
            if result is not None:
                with open('results.csv', 'a') as f:
                    writer = csv.writer(f)
                    writer.writerows(result)
                results.extend(result)
    return results


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=str, default='assets/asian_american.jpg')
    parser.add_argument('--model', type=str, default='FairFace')
    parser.add_argument('--checkpoint', type=str, default='./res34_fairface.pth')
    parser.add_argument('--det_model', type=str, default='RetinaFace')
    parser.add_argument('--det_checkpoint', type=str, default='./mobilenet0.25_Final.pth')
    args = vars(parser.parse_args())

    imgs = pd.read_csv(args['source'])['img_path']
    source = args.pop('source')

    num_processes = 4
    imgs_split = np.array_split(imgs, num_processes)
    with multiprocessing.Pool(num_processes) as p:
        results = p.map(partial(process_images, args=args), imgs_split)
    results = [item for sublist in results for item in sublist]

    with open('results_all.csv', 'w') as f:
        writer = csv.writer(f)
        for row in results:
            writer.writerow(row)