import requests
from bs4 import BeautifulSoup
import os

def extract_mp3_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    buttons = soup.find_all('button', {'data-audio-src': True})
    mp3_links = [button['data-audio-src'] for button in buttons if button['data-audio-src'].startswith("https://ondemand-mp3.dradio.de")]
    return mp3_links

def sanitize_filename(filename):
    return filename.split('?')[0]  # Removes query parameters

def download_file(url, folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

    local_filename = sanitize_filename(url.split('/')[-1])
    path = os.path.join(folder, local_filename)

    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_filename

url = "https://www.deutschlandfunk.de/audiothek"
mp3_links = extract_mp3_links(url)

download_folder = 'data/bronze'  # Folder where the files will be saved

for link in mp3_links:
    filename = download_file(link, download_folder)
    print(f"Downloaded {filename} to {download_folder}")
