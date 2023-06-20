import os
import shutil
import requests
import io
import base64
from PIL import Image, PngImagePlugin
import re


def blip_cap(inputdir="experiments/blip_out", outputfile=""):
    # 打标后直接写入text 用来给gen image函数用
    models = []
    prompts = []
    refimages = []
    for refimage in os.listdir(inputdir):
        name = refimage[8:]
        # print(name)
        if name[-3:] == 'txt':
            print(name)
            with open(os.path.join(inputdir, refimage), 'r') as file:
                prompt = file.read()
            models.append("StableDiffusion")
            refimages.append(name.replace('txt','png'))
            prompts.append(prompt)
    with open(outputfile, 'w', encoding='utf-8') as f:
        for modelname, prompt, refimage in zip(models, prompts, refimages):
            line = f"{refimage}\t{modelname}\t{prompt}\n"
            f.write(line)

blip_cap(inputdir="experiments/blip_out", outputfile="experiments/blipcap.txt")


def flamingo_cap(inputfile='prompt_gen.txt', outputfile='our_gen.txt'):

    files = {}
    with open('./prompts_1k.txt', 'r', encoding='utf-8') as f:
        for index, line in enumerate(f):
            parts = line.strip()
            files[parts] = str(index)+'.png'

    answers = {}
    with open(inputfile, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('\t')
            key = parts[0]
            values = parts[1]
            answers[key] = values
    models = []
    prompts = []
    refimages = []
    for refimage, answer in answers.items():
        pattern = r'using (\w+) and'
        match = re.search(pattern, answer)
        if match:
            word = match.group(1)
            split_string = answer.split(":")
            prompt = split_string[1].strip()
            if len(prompt)>0:
                models.append(word)
                refimages.append(refimage)
                prompts.append(prompt)
        else:
            print(answer)

    zipped = list(zip(models, prompts, refimages))
    zipped.sort()
    models, prompts, refimages = zip(*zipped)
    with open(outputfile, 'w', encoding='utf-8') as f:
        for modelname, prompt, refimage in zip(models, prompts, refimages):
            line = f"{files[refimage]}\t{modelname}\t{prompt}\n"
            f.write(line)



flamingo_cap(inputfile='our_promptgen.txt', outputfile='our_gen.txt')





def generate(prompt_file, outdir, batchsize=5):
    url = "http://127.0.0.1:7860"
    ckpt_ext = ["StableDiffusion", "NovelAI", "AnythingV5", "ACertainModel", "StbleDiffusion"]

    models = []
    prompts = []
    refimages = []
    with open(prompt_file, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('\t')
            refimages.append(parts[0])
            models.append(parts[1])
            prompts.append(parts[2])

    for modelname, prompt, refimage in zip(models, prompts, refimages):
        dirname = os.path.splitext(os.path.basename(refimage))[0]
        if modelname in ckpt_ext:
            ext = ".ckpt"
        else:
            ext = ".safetensors"
        input_model = modelname + ext

        if not os.path.exists(os.path.join(outdir, str(dirname))):
            os.mkdir(os.path.join(outdir, str(dirname)))
        if len(os.listdir(os.path.join(outdir, str(dirname))))<batchsize:
            print(modelname)
            opt = requests.get(url=f'{url}/sdapi/v1/options')
            opt_json = opt.json()
            print(opt_json['sd_model_checkpoint'])
            opt_json['sd_model_checkpoint'] = input_model
            requests.post(url=f'{url}/sdapi/v1/options', json=opt_json)
            payload = {
                "sd_model_checkpoint": input_model,
                "CLIP_stop_at_last_layers": 2,
                "prompt": prompt,
                "steps": 20,
                "seed": -1,
                "batch_size": batchsize,
                "cfg_scale": 7,
                "width": 512,
                "height": 512,
                "negative_prompt": "bad anatomy, low quality, worst quality, blurry, text, watermark, normal quality, ugly, lowres, signature",
                "sampler_index": "DPM++ 2M Karras"
            }
            response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=payload)
            r = response.json()
            for idx, i in enumerate(r['images']):
                image = Image.open(io.BytesIO(base64.b64decode(i.split(",",1)[0])))
                png_payload = {"image": "data:image/png;base64," + i}
                response2 = requests.post(url=f'{url}/sdapi/v1/png-info', json=png_payload)
                pnginfo = PngImagePlugin.PngInfo()
                pnginfo.add_text("parameters", response2.json().get("info"))
                image.save(os.path.join(outdir, str(dirname),'output{}.png'.format(idx)), pnginfo=pnginfo)


generate("experiments/blipcap.txt", "experiments/blip", batchsize=10)















