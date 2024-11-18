# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    spider.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: maott <maott@student.42.fr>                +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/11/18 11:07:35 by maott             #+#    #+#              #
#    Updated: 2024/11/18 18:01:34 by maott            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import os
import argparse
import requests
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"

DEFAULT_DEPTH = 5
DEFAULT_PATH = Path("./data")
IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".gif", ".bmp")

def parse_arguments():
    parser = argparse.ArgumentParser(description="The spider program allows you to extract all images from a website recursively by providing a URL as a parameter.")

    parser.add_argument('-r', action='store_true', help='recursively downloads the images in a URL received as a parameter.')
    parser.add_argument('-l', type=int, metavar='[N]', help='indicates the maximum depth level of the recursive download. If not indicated, it will be 5.')
    parser.add_argument('-p', metavar='[PATH]', help='indicates the path where the downloaded files will be saved. If not specified, ./data/ will be used.')
    parser.add_argument('url', help='The URL to be processed.')

    args = parser.parse_args()

    if args.r:
        args.l = args.l if args.l is not None else DEFAULT_DEPTH
    else:
        args.l = 1

    args.p = Path(args.p) if args.p else DEFAULT_PATH

    if args.p.is_absolute():
        print(f"{YELLOW}Warning: The path must be relative to the current directory. Now, the default path will be used: {DEFAULT_PATH}{RESET}")
        args.p = DEFAULT_PATH
    elif not args.p.exists():
        args.p.mkdir(parents=True, exist_ok=True)

    if not urlparse(args.url).scheme or not urlparse(args.url).netloc:
        print(f"{RED}Error: Invalid URL format.{RESET}")
        exit(1)

    return args

def download_image(url, path):
    filename = os.path.basename(url)
    filepath = os.path.join(path, filename)

    if os.path.exists(filepath):
        print(f"{YELLOW}File already exists: {filepath}{RESET}")
        return

    try:
        response = requests.get(url, stream=True, timeout=10)
        if response.status_code != 200:
            print(f"{RED}Failed to download: {url}{RESET}")
            return

        with open(filepath, 'wb') as file:  # w = write, b = binary mode
            file.write(response.content)
            print(f"{GREEN}Downloaded: {filepath}{RESET}")

    except requests.exceptions.RequestException as e:
        print(f"{RED}Error downloading {url}: {e}{RESET}")

def extract_images(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    images = []

    for img in soup.find_all('img'):
        img_url = img.get('src')
        if img_url and img_url.endswith(IMAGE_EXTENSIONS):
            full_url = urljoin(url, img_url)
            images.append(full_url)

    return images

def scrape_images(url, path, max_depth, depth):
    print(f"Scraping: {url} (depth: {depth})")

    images = extract_images(url)
    for img_url in images:
        download_image(img_url, path)

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    if depth + 1 >= max_depth:
        return

    for link in soup.find_all('a', href=True):
        href = link.get('href')
        if href and not href.startswith('#'):
            full_url = urljoin(url, href)
            if urlparse(full_url).netloc == urlparse(url).netloc:
                scrape_images(full_url, path, max_depth, depth + 1)

def main():
    args = parse_arguments()
    scrape_images(args.url, args.p, args.l, depth = 1)

if __name__ == "__main__":
    main()
