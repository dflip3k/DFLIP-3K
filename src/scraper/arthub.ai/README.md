# arthub.ai

All raw data I scrape in "data" file.  
Just load this file.  
But we need to download images by url provided.  
Prompts and parameters already saved in data.

The sturcture of data is python "Dict", I just pickle dump it.

A sample form dictionary of key 62551:  

['https://arthub.ai/art/62551', 'https://img5.arthub.ai/user-uploads/ae622f8f255c108461737a228cc6ccd897601514/4270b62b-213d-4dff-8174-f43504241e77/ah3-709f643279fc.jpeg', {'Seed': 65650, 'Scale': 7.22, 'Steps': 25, 'Img Width': 512, 'Img Height': 768, 'model_version': 'DiffusionBeecustom_DreamShaper_4BakedVae'}, 'Serenay Sarıkaya, intricate high detail, dramatic, skin pores, very dark lighting, heavy shadows, detailed, (vibrant, photo realistic, dramatic, dark, sharp focus) ((film grain, skin details, high detailed skin texture, 8k hdr, dslr))']


I wirte a python download script to automatic download all images.
with key.XXX as file name. easy to find corresponding.



I have to say, the quality of images from this website is low.

Some of them are high quality.

Many pictures don't have negative prompts and model parameters.

Some pictures even don't have prompts.

Cleaning it.
