import requests


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


all_hash = []
with open('utils/hash2num.txt', 'r') as f:
    for line in f:
        columns = line.split()
        if columns:
            all_hash.append(columns[0])

from tqdm import tqdm
success_files = []
for id, hash_string in tqdm(enumerate(all_hash)):
    try:
        download_urls = get_download_urls(hash_string)
        if download_urls:
            success_files.append('{}\t{}\n'.format(hash_string, download_urls))
    except:
        print("ERROR")



with open('model_urls.txt', 'a') as f:
    for ii in success_files:
        f.write(ii.split()[1]+'\n')
