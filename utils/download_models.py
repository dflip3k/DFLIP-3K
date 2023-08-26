import requests
import json

def get_download_urls(hash_string):
    # Construct the API URL
    url = f"https://civitai.com/api/v1/model-versions/by-hash/{hash_string}"

    # Send the GET request
    response = requests.get(url)

    # Ensure the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Get the "downloadUrl" field values for each file
        download_urls = [file.get("downloadUrl") for file in data.get("files", [])]

        # Return the "downloadUrl" field values
        return download_urls[0]
    else:
        return False

# all_hash = []
# with open('utils/hash2num.txt', 'r') as f:
#     for line in f:
#         columns = line.split()
#         if columns:
#             all_hash.append(columns[0])
#

def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

raw_jsoon_path = r'D:\workspace\hug\storage\pd.json'
raw_jsoon = read_json_file(raw_jsoon_path)
sdftpart = {}
for key, item in raw_jsoon.items():
    if "Model hash" in item:
        model_hash = item["Model hash"]
        if model_hash not in sdftpart:
            sdftpart[model_hash] = 1
        else:
            sdftpart[model_hash]+=1

import operator
sorted_d = dict(sorted(sdftpart.items(), key=operator.itemgetter(1), reverse=True))

from tqdm import tqdm
success_files = []
for id, hash_string in tqdm(enumerate(sorted_d.keys())):
    try:
        download_urls = get_download_urls(hash_string)
        if download_urls:
            success_files.append('{}\t{}\n'.format(hash_string, download_urls))
    except:
        print("ERROR")







with open('model_urls.txt', 'w') as f:
    for ii in success_files:
        f.write(ii)

allhash = []
for i in success_files:
    allhash.append(i.split('\t')[0])



success_files2 = []
for id, hash_string in tqdm(enumerate(sorted_d.keys())):
    if hash_string not in allhash:
        success_files2.append('{}\t{}\n'.format(hash_string, 'None'))


with open('model_urls.txt', 'a') as f:
    for ii in success_files2[:942]:
        f.write(ii)