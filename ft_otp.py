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
import re
import time
import struct
import hmac
import hashlib
import base64

RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"

FT_OTP_KEY_FILE = "ft_otp.key"
TIME_STEP = 30

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

def encrypt_and_store_key(hex_key):
    hex_key_bytes = bytes.fromhex(hex_key)
    encoded_key = base64.urlsafe_b64encode(hex_key_bytes)

    try:
        with open(FT_OTP_KEY_FILE, 'wb') as file:
            file.write(encoded_key)

    except Exception as e:
        print(f"{RED}Error: Could not write to file '{FT_OTP_KEY_FILE}': {e}{RESET}")
        exit(1)

    print(f"{GREEN}Key was successfully saved in {FT_OTP_KEY_FILE}.{RESET}")

def decrypt_key(file_path):
    try:
        with open(file_path, 'rb') as file:
            encoded_key = file.read().strip()

    except Exception as e:
        print(f"{RED}Error: Could not read from file '{file_path}': {e}{RESET}")
        exit(1)

    hex_key_bytes = base64.urlsafe_b64decode(encoded_key)

    return hex_key_bytes

def generate_otp(hex_key_bytes):
    time_step = int(time.time() // TIME_STEP)
    time_bytes = struct.pack(">Q", time_step)

    # Step 1: Generate an HMAC-SHA-1 value (a 20-byte string)
    hmac_sha1 = hmac.new(hex_key_bytes, time_bytes, hashlib.sha1)
    hmac_sha1_bytes = hmac_sha1.digest()

    # Step 2: Generate a 4-byte string (Dynamic Truncation)
    offset = hmac_sha1_bytes[-1] & 0x0F
    bin_code = (hmac_sha1_bytes[offset] & 0x7F) << 24 \
           | (hmac_sha1_bytes[offset + 1] & 0xFF) << 16 \
           | (hmac_sha1_bytes[offset + 2] & 0xFF) << 8 \
           | (hmac_sha1_bytes[offset + 3] & 0xFF)

    otp = bin_code % (10 ** 6)
    otp = str(otp).zfill(6)

    return otp

def parse_arguments():
    parser = argparse.ArgumentParser(description="ft_otp")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-g', metavar='[FILE]', type=str, help='Generates and saves an encrypted ft_otp.key file')
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

def main():
    args, file_path = parse_arguments()

    if args.g:
        hex_key = validate_hex_key(file_path)
        encrypt_and_store_key(hex_key)

    elif args.k:
        hex_key = decrypt_key(file_path)
        otp = generate_otp(hex_key)

        print(f"{GREEN}{otp}{RESET}")

if __name__ == "__main__":
    main()
