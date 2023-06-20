import json
import requests

response = requests.get('https://civitai.com/api/v1/model-versions/by-hash/a074b8864e')
data = json.loads(response.text)

hash2name = {}
with open('hash2name2.txt', 'r') as f:
    for line in f:
        parts = line.strip().split(' ')
        key = parts[0]
        values = parts[1]
        response = requests.get('https://civitai.com/api/v1/model-versions/by-hash/'+str(key))
        data = json.loads(response.text)
        if 'error' not in data:
            hash2name[key] = "{}\t{}".format(data['model']['name'],data['downloadUrl'])
        else:
            hash2name[key] = "{}".format(values)

with open('hash_name_url.txt', 'w', encoding='utf-8') as f:
    for key, value in hash2name.items():
        line = f"{key} {value}\n"
        f.write(line)


hash2name = {}
with open('hash2name2.txt', 'r') as f:
    for line in f:
        parts = line.strip().split(' ')
        key = parts[0]
        values = parts[1]
        response = requests.get('https://civitai.com/api/v1/model-versions/by-hash/'+str(key))
        data = json.loads(response.text)
        if 'error' not in data:
            hash2name[key] = "{}\t{}\t{}".format(data['model']['name'],data['modelId'],data['downloadUrl'])
        else:
            hash2name[key] = "{}".format(values)






hash2name = {}
with open('hash2name2.txt', 'r') as f:
    for line in f:
        parts = line.strip().split(' ')
        key = parts[0]
        values = parts[1]
        response = requests.get('https://civitai.com/api/v1/model-versions/by-hash/'+str(key))
        data = json.loads(response.text)
        if 'error' not in data:
            hash2name[key] = "{}".format(data['modelId'])
        else:
            hash2name[key] = "{}".format(values)


with open('modelID.txt', 'w', encoding='utf-8') as f:
    for key, value in hash2name.items():
        line = f"{value}\n"
        f.write(line)


import json
import requests

hash2name = {}
with open('hash2num.txt', 'r') as f:
    for line in f:
        parts = line.strip().split(' ')
        key = parts[0]
        values = parts[1]
        if key in hash2name:
            continue
        response = requests.get('https://civitai.com/api/v1/model-versions/by-hash/'+str(key))
        data = json.loads(response.text)
        if 'error' not in data:
            if 'downloadUrl' not in data:
                downloadUrl = ' '
            else:
                downloadUrl = data['downloadUrl']
            hash2name[key] = "{}\t{}\t{}\t{}".format(data['model']['name'],data['id'],data['modelId'],downloadUrl)
            print(hash2name[key])
        else:
            hash2name[key] = "{}".format(values)



import numpy as np
hashsearch = np.load('datasets/civitai/hashsearch.npy',allow_pickle=True).item()

ids, modelids = {},{}
for key, value in hashsearch.items():
    try:
        name, id, modelid, url = value.split('\t')
        ids[key] = id
        modelids[key] = modelid
    except:
        print(key)


# 以modelid为主
hash2modelids = modelids
modelids2hash = {}
for key, value in hash2modelids.items():
    if value in modelids2hash:
        modelids2hash[value].append(key)
    else:
        modelids2hash[value] = [key]


modelid2num = {}
with open('hash2num.txt', 'r') as f:
    for line in f:
        parts = line.strip().split(' ')
        key = parts[0]
        values = parts[1]
        if key in hash2modelids:
            if hash2modelids[key] not in modelid2num:
                modelid2num[hash2modelids[key]] = int(values)
            else:
                modelid2num[hash2modelids[key]] += int(values)


with open('hash2num_supermodel.txt', 'w', encoding='utf-8') as f:
    for key, value in modelid2num.items():
        for hash in modelids2hash[key]:
            line = f"{hash} {value}\n"
            f.write(line)


hash2num = {}
with open('hash2num.txt', 'r') as f:
    for line in f:
        parts = line.strip().split(' ')
        key = parts[0]
        values = parts[1]
        hash2num[key] = values


hash2num_s = {}
with open('hash2num_supermodel.txt', 'r') as f:
    for line in f:
        parts = line.strip().split(' ')
        key = parts[0]
        values = parts[1]
        hash2num_s[key] = values


with open('hash2num_superall.txt', 'w', encoding='utf-8') as f:
    for key, value in hash2num.items():
        if key in hash2num_s:
            line = f"{key} {hash2num_s[key]}\n"
            f.write(line)
        else:
            line = f"{key} {value}\n"
            f.write(line)

import numpy as np
hashsearch = np.load('datasets/civitai/hashsearch.npy',allow_pickle=True).item()

alllines = []
with open('hash2num_superall.txt', 'r') as f:
    for line in f:
        parts = line.strip().split(' ')
        key = parts[0]
        values = parts[1]
        if int(values)>200:
            if len(hashsearch[key].split('\t')) > 1:
                name, id, mid, url = hashsearch[key].split('\t')
                alllines.append("{}\t{}\n".format(key, name))
            else:
                alllines.append("{}\t{}\n".format(key, values))

sorted_lines = sorted(alllines, key=lambda x: x.split('\t')[1])

with open('trainhash.txt', 'w', encoding='utf-8') as f:
    for line in sorted_lines:
        f.write(line)






import numpy as np
hashsearch = np.load('datasets/civitai/hashsearch.npy',allow_pickle=True).item()

hash_modelid = {}
with open('trainhash.txt', 'r') as f:
    for line in f:
        parts = line.split()
        key = parts[0]
        values = parts[1]
        hash_modelid[key] = values




with open('_write.txt', 'w', encoding='utf-8') as f:
    for key, name in hash_modelid.items():
        if key in hashsearch:
            url = hashsearch[key].split()[-1]
            line = "{}\t{}\t{}\n".format(key, name, url)
            f.write(line)
        else:
            line = "{}\t{}\n".format(key, name)
            f.write(line)


with open('_urlfiles.txt', 'w', encoding='utf-8') as f:
    for key, name in hash_modelid.items():
        if key in hashsearch:
            url = hashsearch[key].split()[-1]
            line = "{}\n".format(url)
            f.write(line)
        else:
            pass

