#!/usr/bin/env python3

# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    ft_otp.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: maott <maott@student.42.fr>                +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/11/19 13:00:20 by maott             #+#    #+#              #
#    Updated: 2024/11/19 13:52:30 by maott            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import argparse
import os
import re   # regular expression
from cryptography.fernet import Fernet

RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"

FT_OTP_KEY_FILE = "ft_otp.key"
FERNET_KEY_FILE = ".fernet.key"

def parse_arguments():
    parser = argparse.ArgumentParser(description="ft_otp")

    # Create a mutually exclusive group for -g and -k
    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument('-g', metavar='[FILE]', type=str, help='Generates an encrypted ft_otp.key file')
    group.add_argument('-k', metavar='[FILE]', type=str, help='Generates a one-time password using the ft_otp.key file')

    args = parser.parse_args()

    if args.g:
        file_path = args.g
    elif args.k:
        file_path = args.k

    if not os.path.isfile(file_path):
        print(f"{RED}Error: '{file_path}' is not a valid file path or does not exist.{RESET}")
        exit(1)

    if not os.access(file_path, os.R_OK):
        print(f"{RED}Error: '{file_path}' is not readable. Check permissions.{RESET}")
        exit(1)

    return args, file_path

def validate_hex_key(file_path):
    try:
        with open(file_path, 'r') as file:
            hex_key = file.read().strip()

    except Exception as e:
        print(f"{RED}Error: Failed to read file: {e}{RESET}")
        exit(1)

    if len(hex_key) < 64:
        print(f"{RED}Error: Key must be at least 64 hexadecimal characters.{RESET}")
        exit(1)

    if not re.fullmatch(r'[0-9a-fA-F]+', hex_key):
        print(f"{RED}Error: Key must only contains hexadecimal characters.{RESET}")
        exit(1)

    return hex_key

def read_file(file_path, mode="rb"):
    try:
        with open(file_path, mode) as file:
            return file.read()

    except Exception as e:
        print(f"{RED}Error: Could not read from file '{file_path}': {e}{RESET}")
        exit(1)

def write_file(file_path, data, mode="wb"):
    try:
        with open(file_path, mode) as file:
            file.write(data)

    except Exception as e:
        print(f"{RED}Error: Could not write to file '{file_path}': {e}{RESET}")
        exit(1)

def generate_key(hex_key):
    # Check if the Fernet key exists, if not, create a new one
    if os.path.exists(FERNET_KEY_FILE):
        print(f"{GREEN}Found existing Fernet key file. Using the existing key.{RESET}")
        fernet_key = read_file(FERNET_KEY_FILE)
    else:
        fernet_key = Fernet.generate_key()
        write_file(FERNET_KEY_FILE, fernet_key)
        print(f"{GREEN}New Fernet key generated and saved in {FERNET_KEY_FILE}.{RESET}")

    # Encrypt the hexadecimal key using the Fernet key
    cipher = Fernet(fernet_key)
    encrypted_key = cipher.encrypt(hex_key.encode())
    write_file(FT_OTP_KEY_FILE, encrypted_key)
    print(f"{GREEN}Key was successfully saved in {FT_OTP_KEY_FILE}.{RESET}")

def generate_otp(file_path):
    # Ensure Fernet key file exists
    if not os.path.isfile(FERNET_KEY_FILE):
        print(f"{RED}Error: '{FERNET_KEY_FILE}' is missing. Please generate a key first using the -g option.{RESET}")
        exit(1)

    # Read the Fernet key and the encrypted hex key
    fernet_key = read_file(FERNET_KEY_FILE)
    encrypted_key = read_file(file_path)

    # Decrypt the hex key
    cipher = Fernet(fernet_key)
    hex_key = cipher.decrypt(encrypted_key).decode()

    print(f"Decrypted key: {hex_key}")

def main():
    args, file_path = parse_arguments()

    if args.g:
        hex_key = validate_hex_key(file_path)
        generate_key(hex_key)
    elif args.k:
        generate_otp(file_path)

if __name__ == "__main__":
    main()
