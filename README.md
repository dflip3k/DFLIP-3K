# DFLIP-3K

[![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC_BY--NC_4.0-brightgreen.svg)](https://creativecommons.org/licenses/by-nc/4.0/) ![Release .10](https://img.shields.io/badge/Release-1.0-brightgreen) ![PyTorch](https://img.shields.io/badge/PyTorch-2.0-brightgreen) ![Python](https://img.shields.io/badge/Python-3.10-brightgreen)


<p align="center">
<br>
  <a href="" target="_blank"> Paper </a >  •  <a href=""> Data </a > <br>  •  <a href=""> Methods </a > <br>
<br>
</p >


Welcome to *DFLIP-3K*, a deepfake database (DFLIP-3K) for the development of convincing and explainable deepfake detection:

> ✅ **3K+ generative models**: *DFLIP-3K* provides deepfake images generated by at leasts 3K+ generative models.
> 
> ✅ **Inguistic footprints of these deepfakes**: *DFLIP-3K* offers an integrated framework for the implementation of state-of-the-art detection methods.
> 
> ✅ **Standardized Evaluations**: *DFLIP-3K* introduces standardized evaluation metrics and protocols to enhance the transparency and reproducibility of performance evaluations.
> 
> ✅ **Open database**: *DFLIP-3K* is an open database that fosters transparency and encourages collaborative efforts to 
further enhance its growth.


<font size=5><center><b> 📋 Table of Contents </b> </center></font>

- [Linguistic Profiling of Deepfakes: An Open Database
for Next-Generation Deepfake Detection](#Linguistic-Profiling-of-Deepfakes-An-Open-Database-for-Next-Generation-Deepfake-Detection)
  - [Features](#features)
  - [Quick Start](#quick-start)
    - [Download Data](#download-data)
    - [Preprocessing](#preprocessing)
    - [Training](#training)
---
[comment]: <> (  - [Installation]&#40;#installation&#41;)


## 📚 Features
<a href="#top">[Back to top]</a>

DFLIP-3K has the following features:

⭐️  DFLIP-3K database encompasses approximately **300K** deepfake samples produced from about **3K** generative models.   
⭐️  **190K** textual prompts that are used to create images.   
⭐️  Linguistic profiling in simultaneous deepfake detection, identification, and prompt prediction. 

DFLIP-3K will be continuously updated to track the latest advances in deepfake.

The collection of DFLIP-3K and implementations of detection methods is an ongoing project. 

**You are welcome to contribute your methods and data to DFLIP-3K.**

## Visualization
The project page displays a limited selection of DFLIP-3K samples, comprising images and prompts.
https://dflip3k.github.io/DFLIP-3K/




## ⏳ Quick Start

### 1. Download Data

<a href="#top">[Back to top]</a>

Please download metadata we proveded from this [URL](https://github.com/dflip3k/storage).
Metadata is stored in this repository in JSON format.
Upon downloading metadata, please ensure to store them in the [`./datasets`](./datasets/) folder.


Once you have downloaded metadata, you can proceed with running the following line to download image:

Note that it may fail several times due to unstable network connections, but the script can be restarted and downloaded files will not be re-downloaded.

```
cd utils

python downloader.py --meta_file [Path to JSON file].json --save_dir [where to save iamges]
```

```
datasets
├── downloaded
│   ├── mj
│   │  ├──*.jpg
│   │  └──*.png
│   ├── sd
│   │  ├──*.jpg
│   │  └──*.png
│   ├── pd
│   ├── dalle
│   └── ...
├── pd.json
└── ...
```


### 2. Preprocessing

<a href="#top">[Back to top]</a>

After downloading all data, we strongly recommend that you convert all images to the same format (such as PNG in our dataset). This will facilitate reducing errors caused by different image formats during the loading process. However, this is optional.


### 3. Pretrained Weights

<a href="#top">[Back to top]</a>

Please wait a moment.


### 4. Training

<a href="#top">[Back to top]</a>

We give Otter based implementation for deepfake detection, identification and prompt prediction tasks.

```
git clone https://github.com/dflip3k/Otter

cd Otter 




```









