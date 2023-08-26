https://github.com/fudan-zvg/Semantic-Segment-Anything
SAM is a powerful model for arbitrary object segmentation, while SA-1B is the largest segmentation dataset to date. However, SAM lacks the ability to predict semantic categories for each mask. (I) To address above limitation, we propose a pipeline on top of SAM to predict semantic category for each mask, called Semantic Segment Anything (SSA). (II) Moreover, our SSA can serve as an automated dense open-vocabulary annotation engine called Semantic segment anything labeling engine (SSA-engine), providing rich semantic category annotations for SA-1B or any other dataset. This engine significantly reduces the need for manual annotation and associated costs.



https://github.com/facebookresearch/segment-anything



Please follow above link to install and run

```
git clone git@github.com:fudan-zvg/Semantic-Segment-Anything.git
cd Semantic-Segment-Anything
conda env create -f environment.yaml
conda activate ssa
python -m spacy download en_core_web_sm
# install segment-anything
cd ..
git clone git@github.com:facebookresearch/segment-anything.git
cd segment-anything; pip install -e .; cd ../Semantic-Segment-Anything`
```


python scripts/main_ssa_engine.py --data_dir=/home/teddy/workspace/datasets/aiart/sdft --out_dir=output --world_size=4 --save_img --sam --ckpt_path=./sam_vit_h_4b8939.pth



# https://github.com/fudan-zvg/Semantic-Segment-Anything




download  https://drive.google.com/file/d/11i8pKctxz3wVkDBlWKvhYIh7kpVFXSZ4/view?usp=drive_link

install
https://github.com/WildChlamydia/MiVOLO

pip install -r requirements.txt
pip install .

python3 demo.py \
--input /home/teddy/workspace/datasets/aiart/sdft \
--output ./out_sdft \
--detector-weights "models/yolov8x_person_face.pt " \
--checkpoint "models/mivolo_imbd.pth.tar" \
--device "cuda:2" \
--with-persons \
--draw




# put predict.py under EasyFace 

run

`python predict.py --source parti.csv --model FairFace --det_model RetinaFace
`




There are also some awesome works:

https://github.com/RockeyCoss/Prompt-Segment-Anything
https://github.com/segments-ai/panoptic-segment-anything
https://github.com/UX-Decoder/Semantic-SAM
https://github.com/zhenyuw16/UniDetector