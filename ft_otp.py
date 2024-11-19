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

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-g', action='store_true', help='generates an encrypted ft_otp.key file based on the hexadecimal key given as file argument')
    group.add_argument('-k', action='store_true', help='generates an one-time password based on the ft_otp.key file given as argument')

    parser.add_argument('file', type=str, help='file containing the key or OTP')

    args = parser.parse_args()

    if not os.path.isfile(args.file):
        print(f"{RED}error: '{args.file}' is not a valid file path or does not exist.{RESET}")
        exit(1)

    if not os.access(args.file, os.R_OK):
        print(f"{RED}error: '{args.file}' is not readable. Check permissions.{RESET}")
        exit(1)

    return args

def validate_hex_key(file_path):
    try:
        with open(file_path, 'r') as file:
            hex_key = file.read().strip()

    except Exception as e:
        print(f"{RED}error: Failed to read file: {e}{RESET}")
        exit(1)

    if len(hex_key) < 64:
        print(f"{RED}error: key must be at least 64 hexadecimal characters.{RESET}")
        exit(1)

    if not re.fullmatch(r'[0-9a-fA-F]+', hex_key):
        print(f"{RED}error: key must only contains hexadecimal characters.{RESET}")
        exit(1)

    return hex_key

def generate_key(hex_key):
    if os.path.exists(FERNET_KEY_FILE):
        with open(FERNET_KEY_FILE, "rb") as fernet_key_file:
            fernet_key = fernet_key_file.read()
    else:
        fernet_key = Fernet.generate_key()
        with open(FERNET_KEY_FILE, "wb") as fernet_key_file:
            fernet_key_file.write(fernet_key)

    cipher = Fernet(fernet_key)
    encrypted_key = cipher.encrypt(hex_key.encode())

    with open(FT_OTP_KEY_FILE, "wb") as ft_otp_key_file:
        ft_otp_key_file.write(encrypted_key)

    print(f"{GREEN}Key was successfully saved in ft_otp.key.{RESET}")

def generate_otp(file_path):
    if not os.path.isfile(FERNET_KEY_FILE):
        print(f"{RED}error: '{FERNET_KEY_FILE}' is missing.{RESET}")
        exit(1)

    with open(FERNET_KEY_FILE, "rb") as fernet_key_file:
        encryption_key = fernet_key_file.read()

    with open(file_path, "rb") as ft_otp_key_file:
        encrypted_key = ft_otp_key_file.read()

    cipher = Fernet(encryption_key)
    hex_key = cipher.decrypt(encrypted_key).decode()

    print(f"Decrypted key: {hex_key}")

def main():
    args = parse_arguments()

    if args.g:
        hex_key = validate_hex_key(args.file)
        generate_key(hex_key)
    elif args.k:
        generate_otp(args.file)

if __name__ == "__main__":
    main()
