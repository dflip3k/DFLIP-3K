import os
import requests
import time

# Open the file containing the URLs
with open('urls.txt') as f:
    urls = f.readlines()

# Remove any whitespace or newline characters from the URLs
urls = [url.strip() for url in urls]

# Set the directory where you want to save the downloaded files
save_dir = 'downloads/'

# Create the save directory if it doesn't already exist
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

headers = {}
headers["Upgrade-Insecure-Requests"] = '1'
headers[
    "User-Agent"] = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'


already_downloaded = list(os.walk(save_dir))
# Loop through each URL and download the corresponding file
for url in urls:
    print(url)
    # Extract the filename from the URL
    filename = os.path.basename(url).split('.')[0] + '.png'
    # Construct the full path to save the file
    save_path = os.path.join(save_dir, filename)

    if filename not in already_downloaded[0][2]:
        response = requests.get(url, headers=headers)
        with open(save_path, 'wb') as f:
            f.write(response.content)
        time.sleep(2)
