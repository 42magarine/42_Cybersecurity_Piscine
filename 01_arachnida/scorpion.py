import os
import sys
import stat
import time
import humanize
from PIL import Image
from PIL.ExifTags import TAGS
from pathlib import Path

RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"

def get_exif_data(image_path):
    try:
        # Open the image file
        image = Image.open(image_path)
        exif_data = image._getexif()    # Retrieve EXIF data
        if not exif_data:
            return None

        # Create a dictionary to store EXIF metadata
        metadata = {}
        for tag, value in exif_data.items():
            tag_name = TAGS.get(tag, tag)   # Get human-readable tag names
            metadata[tag_name] = value

        return metadata

    except Exception as e:
        print(f"{RED}Error reading EXIF data from {image_path}: {e}{RESET}")
        return None

def get_file_metadata(image_path):
    try:
        metadata = {}
        file_path = Path(image_path)

        # Populate metadata dictionary with file details
        metadata['Filename'] = file_path.name
        metadata['Directory'] = str(file_path.resolve().parent)
        metadata['File Size'] = humanize.naturalsize(file_path.stat().st_size, binary=True)
        metadata['Creation Date'] = time.ctime(os.path.getctime(image_path))
        metadata['Modification Date'] = time.ctime(os.path.getmtime(image_path))
        metadata['File Permissions'] = stat.filemode(os.stat(image_path).st_mode)

        return metadata

    except Exception as e:
        print(f"{RED}Error getting metadata for {image_path}: {e}{RESET}")
        return None

def display_metadata(image_path):
    # Display basic file metadata
    metadata = get_file_metadata(image_path)
    if metadata:
        print(f"{YELLOW}Basic File Metadata:{RESET}")
        for key, value in metadata.items():
            print(f"{GREEN}{key}: {value}{RESET}")

    # Display EXIF (Exchangeable Image File Format) data
    exif_data = get_exif_data(image_path)
    if exif_data:
        print(f"{YELLOW}EXIF Data:{RESET}")
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
