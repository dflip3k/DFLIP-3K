import pickle
import os
import time
import requests

def data_open(s):
    file = open(s,'rb')
    data = pickle.load(file)
    file.close()
    return data

data = data_open('./data')

# Set the directory where you want to save the downloaded files
save_dir = 'downloads/'

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
for key, value in data.items():
    print(key)
    if str(key) not in already_downloaded:

        url = value[-1]
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            ext = response.headers['Content-Type'].split('/')[-1]
            save_path = os.path.join(save_dir, str(key) + '.' + ext)
            with open(save_path, 'wb') as f:
                f.write(response.content)
            time.sleep(2)
        else:
            url = value[-2]
            response = requests.get(url, headers=headers)
            ext = response.headers['Content-Type'].split('/')[-1]
            save_path = os.path.join(save_dir, str(key) + '.' + ext)
            with open(save_path, 'wb') as f:
                f.write(response.content)
            time.sleep(2)
            print(f"{url} 下载缩略图！")

