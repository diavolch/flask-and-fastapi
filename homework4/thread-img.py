import threading
import time
import argparse
import requests
import os
from tqdm import tqdm
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin, urlparse

threads = []


def get_all_images(url):
    soup = bs(requests.get(url).content, "html.parser")
    urls = []
    for img in soup.find_all("img"):
        img_url = img.attrs.get("src")
        if not img_url:
            continue
        img_url = urljoin(url, img_url)
        try:
            pos = img_url.index("?")
            img_url = img_url[:pos]
        except ValueError:
            pass
        if urlparse(url).netloc and urlparse(url).scheme:
            urls.append(img_url)
    return urls


def download(url, pathname):
    if not os.path.isdir(pathname):
        os.makedirs(pathname)
    response = requests.get(url, stream=True)
    filename = os.path.join(pathname, url.split("/")[-1])
    file_size = int(response.headers.get("Content-Length", 0))
    progress = tqdm(response.iter_content(1024), f"Загружен {filename}", total=file_size, unit="B", unit_scale=True,
                        unit_divisor=1024)
    with open(filename, "wb") as f:
        start_time = time.time()
        for data in progress.iterable:
            f.write(data)
        print(f"Downloaded {filename} in {time.time() - start_time:.2f} seconds")


def main(url):
    path = urlparse(url).netloc
    imgs = get_all_images(url)
    for img in imgs:
        download(img, path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Этот скрипт загружает все изображения с веб‑страницы.")
    parser.add_argument("urls", nargs='+', type=str, help="URL‑адрес веб‑страницы, с которой вы хотите загрузить изображения.")
    args = parser.parse_args()
    urls = args.urls

    for url in urls:
        thread = threading.Thread(target=main, args=[url])
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()