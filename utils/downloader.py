import pickle
import os
import time
import requests
import argparse
import json

def download_func(metadata, save_dir):
    headers = {}
    headers["Upgrade-Insecure-Requests"] = '1'
    headers[
        "User-Agent"] = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
    already_downloaded = list(os.walk(save_dir))[0][2]
    already_downloaded = [i.split('.')[0] for i in already_downloaded]
    # Loop through each URL and download the corresponding file
    for key, value in metadata.items():
        if str(key).split('.')[0] not in already_downloaded:
            url = value['url']
            try:
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    ext = response.headers['Content-Type'].split('/')[-1]
                    save_path = os.path.join(save_dir, str(key) + '.' + ext)
                    with open(save_path, 'wb') as f:
                        f.write(response.content)
                    time.sleep(1)
                    print("Success: {}".format(key))
            except:
                print("Fail: {}".format(url))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download images.')
    parser.add_argument('--meta_file', help='Give me Json file for download')
    parser.add_argument('--save_dir', help='Dir for saving images.')
    args = parser.parse_args()
    # Set the directory where you want to save the downloaded files
    save_dir = args.save_dir
    # Create the save directory if it doesn't already exist
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    metadata = json.load(open(args.meta_file, "r"))
    download_func(metadata, save_dir)




