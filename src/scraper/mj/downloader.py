import pickle
import os
import time
import requests
import warnings
warnings.filterwarnings("ignore")

import json

with open("dalle_up.json") as f:
    data = json.load(f)

save_dir = './'

# Create the save directory if it doesn't already exist
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

headers = {}
headers["Upgrade-Insecure-Requests"] = '1'
headers[
    "User-Agent"] = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'


already_downloaded = list(os.walk(save_dir))[0][2]
already_downloaded = [i.split('.')[0] for i in already_downloaded]

# Loop through each URL and download the corresponding file
for key, item in data.items():
    savefile = key
    if str(savefile) not in already_downloaded:
        url = item['url']
        response = requests.get(url, headers=headers, verify=False)
        if response.status_code == 200:
            ext = response.headers['Content-Type'].split('/')[-1]
            save_path = os.path.join(save_dir, str(savefile) + '.' + ext)
            with open(save_path, 'wb') as f:
                f.write(response.content)
            time.sleep(2)
        else:
            print(f"{url} 错误！")


import json

with open("data3.json") as f:
    data = json.load(f)