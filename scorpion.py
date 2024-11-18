# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    scorpion.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: maott <maott@student.42.fr>                +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/11/18 20:22:09 by maott             #+#    #+#              #
#    Updated: 2024/11/18 20:43:46 by maott            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import os
import sys
from PIL import Image
from PIL.ExifTags import TAGS
from datetime import datetime

RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"

def get_exif_data(image_path):
    try:
        image = Image.open(image_path)
        exif_data = image._getexif()
        if not exif_data:
            return None

        metadata = {}
        for tag, value in exif_data.items():
            tag_name = TAGS.get(tag, tag)
            metadata[tag_name] = value

        return metadata

    except Exception as e:
        print(f"{RED}Error reading EXIF data from {image_path}: {e}{RESET}")
        return None

def get_file_creation_date(image_path):
    try:
        # Get the creation date from the file system metadata
        creation_timestamp = os.path.getctime(image_path)
        creation_date = datetime.fromtimestamp(creation_timestamp).strftime('%Y-%m-%d %H:%M:%S')

        return creation_date

    except Exception as e:
        print(f"{RED}Error getting file creation date for {image_path}: {e}{RESET}")
        return None

def display_metadata(image_path):
    print(f"{GREEN}File: {image_path}{RESET}")

    # Display basic file metadata
    creation_date = get_file_creation_date(image_path)
    if creation_date:
        print(f"{GREEN}Creation Date: {creation_date}{RESET}")

    # Display EXIF (Exchangeable Image File Format) data
    exif_data = get_exif_data(image_path)
    if exif_data:
        print(f"{GREEN}EXIF Data: {RESET}")
        for tag, value in exif_data.items():
            print(f"{GREEN}{tag}: {value}{RESET}")
    else:
        print(f"{YELLOW}No EXIF data found.{RESET}")

def main():
    if len(sys.argv) < 2:
        print(f"{YELLOW}Usage: ./scorpion FILE1 [FILE2 ...]{RESET}")
        sys.exit(1)

    # Loop through each image file passed as an argument
    for image_file in sys.argv[1:]:
        if os.path.isfile(image_file):
            display_metadata(image_file)
        else:
            print(f"{RED}Error: {image_file} is not a valid file.{RESET}")

if __name__ == "__main__":
    main()
