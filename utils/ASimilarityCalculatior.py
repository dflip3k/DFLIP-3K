# from https://huggingface.co/JosephusCheung/ASimilarityCalculatior/blob/main/qwerty.py

from safetensors.torch import load_file
import multiprocessing
import sys
import torch
from pathlib import Path
import torch.nn as nn
import torch.nn.functional as F
import glob
import os
import pickle
import re
import numpy as np
import matplotlib.pyplot as plt


def cal_cross_attn(to_q, to_k, to_v, rand_input):
    hidden_dim, embed_dim = to_q.shape
    attn_to_q = nn.Linear(hidden_dim, embed_dim, bias=False)
    attn_to_k = nn.Linear(hidden_dim, embed_dim, bias=False)
    attn_to_v = nn.Linear(hidden_dim, embed_dim, bias=False)
    attn_to_q.load_state_dict({"weight": to_q})
    attn_to_k.load_state_dict({"weight": to_k})
    attn_to_v.load_state_dict({"weight": to_v})

    return torch.einsum(
        "ik, jk -> ik",
        F.softmax(torch.einsum("ij, kj -> ik", attn_to_q(rand_input), attn_to_k(rand_input)), dim=-1),
        attn_to_v(rand_input)
    )

def model_hash(filename):
    try:
        with open(filename, "rb") as file:
            import hashlib
            m = hashlib.sha256()

            file.seek(0x100000)
            m.update(file.read(0x10000))
            return m.hexdigest()[0:8]
    except FileNotFoundError:
        return 'NOFILE'


def load_model(path):
    if path.suffix == ".safetensors":
        return load_file(path, device="cpu")
    else:
        ckpt = torch.load(path, map_location="cpu")
        return ckpt["state_dict"] if "state_dict" in ckpt else ckpt


def eval(model, n, input):
    qk = f"model.diffusion_model.output_blocks.{n}.1.transformer_blocks.0.attn1.to_q.weight"
    uk = f"model.diffusion_model.output_blocks.{n}.1.transformer_blocks.0.attn1.to_k.weight"
    vk = f"model.diffusion_model.output_blocks.{n}.1.transformer_blocks.0.attn1.to_v.weight"
    atoq, atok, atov = model[qk], model[uk], model[vk]

    attn = cal_cross_attn(atoq, atok, atov, input)
    return attn


def compare_files(file_pair):
    file1, file2 = file_pair
    try:
        model_a = load_model(file1)
    except Exception as e:
        print(f"Error loading {file1}: {e}")
        return

    map_attn_a = {}
    map_rand_input = {}
    for n in range(3, 11):
        try:
            hidden_dim, embed_dim = model_a[
                f"model.diffusion_model.output_blocks.{n}.1.transformer_blocks.0.attn1.to_q.weight"].shape
            rand_input = torch.randn([embed_dim, hidden_dim])
            map_attn_a[n] = eval(model_a, n, rand_input)
        except Exception as e:
            print(f"Error loading {file1}: {e}")
            return
        map_rand_input[n] = rand_input

    del model_a

    try:
        model_b = load_model(file2)
    except Exception as e:
        print(f"Error loading {file2}: {e}")
        return

    sims = []
    for n in range(3, 11):
        try:
            attn_a = map_attn_a[n]
            attn_b = eval(model_b, n, map_rand_input[n])
        except Exception as e:
            print(f"Error loading {file2}: {e}")
            return
        sim = torch.mean(torch.cosine_similarity(attn_a, attn_b))
        sims.append(sim)
    print(f"{file1.name} vs {file2.name}", f"{model_hash(file2)} - {torch.mean(torch.stack(sims)).detach().item() * 1e2:.2f}%")
    return [(f"{file1.name} [{model_hash(file1)}]", f"{file2} [{model_hash(file2)}]"), torch.mean(torch.stack(sims)).detach().item()]

def main():
    folder_path = sys.argv[1]
    files = glob.glob(os.path.join(folder_path, '*'))[:300]

    seed = 114514
    torch.manual_seed(seed)
    print(f"seed: {seed}")

    file_pairs = [(Path(files[i]), Path(files[j])) for i in range(len(files)) for j in range(i+1, len(files))]
    with multiprocessing.Pool(2) as pool:
        result = pool.map(compare_files, file_pairs)

    serialized_dict = pickle.dumps(result)
    with open('all_results.pkl', 'wb') as file:
        file.write(serialized_dict)

def draw_matrix():
    pattern = r'\[([^\]]*)\]'
    with open('all_results.pkl', 'rb') as file:
        serialized = file.read()
    deserialized = pickle.loads(serialized)
    matrix_dict = {}
    row_name = []
    for value in deserialized:
        if value is not None:
            A,B = value[0]
            A = re.findall(pattern, A)[0]
            B = re.findall(pattern, B)[0]
            matrix_dict[(A,B)] = value[1]
            matrix_dict[(B,A)] = value[1]
            row_name.append(A)
            row_name.append(B)
    row_name = list(set(row_name))
    with open('hash.txt', 'w') as f:
        for i, item in enumerate(row_name):
            f.write(str(i) + ' ' + item + '\n')
    num_points = len(row_name)
    dist_matrix = np.zeros((num_points, num_points))
    np.fill_diagonal(dist_matrix, 1)
    for key, dist in matrix_dict.items():
        i = row_name.index(key[0])
        j = row_name.index(key[1])
        dist_matrix[i, j] = dist
    fig, ax = plt.subplots()
    im = ax.imshow(dist_matrix, cmap='hot')
    colorbar = fig.colorbar(im)
    colorbar.ax.set_yticklabels(['{:.0%}'.format(x) for x in colorbar.get_ticks()])
    ax.set_title('Similarity Heatmap')
    fig.tight_layout()
    plt.savefig('myplot.png')


if __name__ == "__main__":
    main()
    draw_matrix()