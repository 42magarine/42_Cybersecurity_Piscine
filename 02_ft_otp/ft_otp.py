#!/usr/bin/env python3

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

# Validates the hexadecimal key from a file.
def validate_hex_key(file_path):
    try:
        with open(file_path, 'r') as file:
            hex_key = file.read().strip()

    except Exception as e:
        print(f"{RED}Error: Failed to read file: {e}{RESET}")
        exit(1)

    # Ensure the key is a valid 64-character hexadecimal string.
    if len(hex_key) < 64 or not re.fullmatch(r'[0-9a-fA-F]+', hex_key) or len(hex_key) % 2 != 0:
        print(f"{RED}Error: Key must be at least 64 hexadecimal characters.{RESET}")
        exit(1)

    return hex_key

# Encrypts the key and stores it in a file.
def encrypt_and_store_key(hex_key):
    hex_key_bytes = bytes.fromhex(hex_key)  # Convert the hex key to bytes
    encoded_key = base64.b32encode(hex_key_bytes)

    try:
        with open(FT_OTP_KEY_FILE, 'wb') as file:
            file.write(encoded_key)

    except Exception as e:
        print(f"{RED}Error: Could not write to file '{FT_OTP_KEY_FILE}': {e}{RESET}")
        exit(1)

    print(f"{GREEN}Key was successfully saved in {FT_OTP_KEY_FILE}.{RESET}")

# Decrypts the key from the stored file.
def decrypt_key(file_path):
    if file_path != FT_OTP_KEY_FILE:
        print(f"{RED}Error: Wrong file, '{FT_OTP_KEY_FILE}'{RESET} is required.")
        exit(1)

    try:
        with open(file_path, 'rb') as file:
            encoded_key = file.read().strip()

    except Exception as e:
        print(f"{RED}Error: Could not read from file '{file_path}': {e}{RESET}")
        exit(1)

    hex_key_bytes = base64.b32decode(encoded_key)

    return hex_key_bytes

# Generates a one-time password (OTP) based on the HMAC-SHA1 algorithm.
def generate_otp(hex_key_bytes):
    time_step = int(time.time() // TIME_STEP)   # Calculate the current time step
    time_bytes = struct.pack(">Q", time_step)   # Pack the time step into 8 bytes

    # Perform HMAC-SHA1 on the key and time step
    hmac_sha1 = hmac.new(hex_key_bytes, time_bytes, hashlib.sha1)
    hmac_sha1_bytes = hmac_sha1.digest()     # Get the raw 20-byte result of the HMAC operation

    # Extract the offset from the last byte of the HMAC result
    # 0x0F is a bitmask with the binary value 00001111
    offset = hmac_sha1_bytes[-1] & 0x0F

    # Combine 4 bytes starting from the offset to form a 32-bit integer
    # 0x7F is a bitmask with the binary value 01111111
    # 0xFF is a bitmask with the binary value 11111111
    bin_code = (hmac_sha1_bytes[offset] & 0x7F) << 24 \
           | (hmac_sha1_bytes[offset + 1] & 0xFF) << 16 \
           | (hmac_sha1_bytes[offset + 2] & 0xFF) << 8 \
           | (hmac_sha1_bytes[offset + 3] & 0xFF)

    # Reduce the binary code to a 6-digit OTP
    otp = bin_code % (10 ** 6)
    otp = str(otp).zfill(6) # Format as a 6-digit string

    return otp

# Parses command-line arguments and ensures the provided file exists and is readable.
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
