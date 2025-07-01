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

visited_urls = set()

def parse_arguments():
    # Create an argument parser with a description
    parser = argparse.ArgumentParser(description="The spider program allows you to extract all images from a website recursively by providing a URL as a parameter.")

    # Define the command-line arguments
    parser.add_argument('-r', action='store_true', help='recursively downloads the images in a URL received as a parameter.')
    parser.add_argument('-l', type=int, metavar='[N]', help='indicates the maximum depth level of the recursive download. If not indicated, it will be 5.')
    parser.add_argument('-p', metavar='[PATH]', help='indicates the path where the downloaded files will be saved. If not specified, ./data/ will be used.')
    parser.add_argument('url', help='The URL to be processed.')

    # Parse the command-line arguments
    args = parser.parse_args()

    # Set the maximum recursion depth if not provided
    if args.r:
        args.l = args.l if args.l is not None else DEFAULT_DEPTH
    else:
        args.l = 1

    # Set the path for saving the files
    args.p = Path(args.p) if args.p else DEFAULT_PATH

    # Check if the path is absolute (if it is, use the default path)
    if args.p.is_absolute():
        print(f"{YELLOW}Warning: The path must be relative to the current directory. Now, the default path will be used: {DEFAULT_PATH}{RESET}")
        args.p = DEFAULT_PATH
    elif not args.p.exists():
        args.p.mkdir(parents=True, exist_ok=True)

    # Check if the provided URL is in a valid format
    if not urlparse(args.url).scheme or not urlparse(args.url).netloc:
        print(f"{RED}Error: Invalid URL format.{RESET}")
        exit(1)

    return args

def sanitize_filename(url):
    # Generate the filename from the URL using the hostname and path
    path = urlparse(url).netloc + urlparse(url).path
    filename = path.replace('/', '_').replace(':', '_').replace('?', '_').replace('&', '_')

    return filename

def download_image(url, path):
    filename = sanitize_filename(url)
    filepath = os.path.join(path, filename)

    # Check if the file already exists
    if os.path.exists(filepath):
        print(f"{YELLOW}File already exists: {filepath}{RESET}")
        return

    try:
        # Try to download the image
        response = requests.get(url, stream=True, timeout=10)
        if response.status_code != 200:
            print(f"{RED}Failed to download: {url}{RESET}")
            return

        # Save the downloaded image
        with open(filepath, 'wb') as file:  # w = write, b = binary mode
            file.write(response.content)
            print(f"{GREEN}Downloaded: {filepath}{RESET}")

    # Catch any errors that occur during the download
    except requests.exceptions.RequestException as e:
        print(f"{RED}Error downloading {url}: {e}{RESET}")

def extract_images(url):
    try:
        # Download the webpage and parse the HTML content
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)

        soup = BeautifulSoup(response.content, 'html.parser')
        images = []

        # Look for <img> tags and check the 'src' attribute for valid image URLs
        for img in soup.find_all('img'):
            img_url = img.get('src')
            if img_url and img_url.endswith(IMAGE_EXTENSIONS):
                full_url = urljoin(url, img_url)  # Construct the full image URL
                images.append(full_url)

        return images

    except requests.exceptions.RequestException as e:
        print(f"{RED}Error retrieving images from {url}: {e}{RESET}")
        return []  # Return an empty list if the request fails

def scrape_images(url, path, max_depth, depth):
    # Check if the URL has already been visited to avoid loops
    if url in visited_urls:
        return
    visited_urls.add(url)

    print(f"Scraping: {url} (depth: {depth})")

    # Extract all images from the page
    images = extract_images(url)
    for img_url in images:
        download_image(img_url, path)

    # Get the page's content and parse it
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Stop recursion if the depth exceeds the max depth
    if depth + 1 > max_depth:
        return

    # Recursively visit all the links on the page
    for link in soup.find_all('a', href=True):
        href = link.get('href')
        full_url = urljoin(url, href)
        if urlparse(full_url).netloc == urlparse(url).netloc:
            scrape_images(full_url, path, max_depth, depth + 1)

def main():
    args = parse_arguments()
    scrape_images(args.url, args.p, args.l, depth = 1)

# Run the program if this script is executed
if __name__ == "__main__":
    main()
