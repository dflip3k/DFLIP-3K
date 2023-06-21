# DFLIP-3K

The emergence of text-to-image generative models has revolutionized the field of deepfakes, 
enabling the creation of realistic and convincing visual content directly from textual descriptions. 
However, this advancement presents considerably greater challenges in detecting the authenticity of such content. 
Existing deepfake detection datasets and methods often fall short in effectively capturing the extensive range of 
emerging deepfakes and offering satisfactory explanatory information for detection. 
To address the significant issue, this paper introduces a deepfake database (DFLIP-3K) for 
the development of convincing and explainable deepfake detection. It encompasses about 300K diverse 
deepfake samples from approximately 3K generative models, which boasts the largest number of deepfake models 
in the literature. Moreover, it collects around 190K linguistic footprints of these deepfakes. The two 
distinguished features enable DFLIP-3K to develop a benchmark that promotes 
progress in linguistic profiling of deepfakes, which includes three sub-tasks namely 
deepfake detection, model identification, and prompt prediction. The deepfake 
model and prompt are two essential components of each deepfake, and thus dissecting them linguistically allows for an invaluable exploration of trustworth and 
interpretable evidence in deepfake detection, which we believe is the key for the 
next-generation deepfake detection. Furthermore, DFLIP-3K is envisioned as an 
open database that fosters transparency and encourages collaborative efforts to 
further enhance its growth. Our extensive experiments on the developed benchmark 
verify that our DFLIP-3K database is capable of serving as a standardized resource 
for evaluating and comparing linguistic-based deepfake detection, identification, and prompt prediction techniques.

## Usage
Metadata is stored in this repository in JSON format:
https://github.com/dflip3k/storage

The repository only contains the tools used for processing the data. 







<table style="width:100%">
<thead>
<tr>
<th style="width:70%" align="center" >Image</th>
<th style="width:30%" align="center">Parameters</th>
</tr>
</thead>
<tbody>
<tr>
<td style="word-break: break-all;" align="right"><img src="https://liblibai-online.liblibai.com/web/6483319f361aa.png?image_process=format,webp&x-oss-process=image/resize,w_600,m_lfit/format,webp"></td>
<td style="word-break: break-all;" align="right"><b>Prompt:</b> asdfasdfasdfasdfasdfasdfasdfasdfasdfasdasdfasdfasdfasdfasdfasdfasdfasdfasdfasdasdfasdfasdfasdfasdfasdfasdfasdfasdfasdasdfasdfasdfasdfasdfasdfasdfasdfasdfasdasdfasdfasdfasdfasdfasdfasdfasdfasdfasdasdfasdfasdfasdfasdfasdfasdfasdfasdfasd </td>
</tbody>
</table>
