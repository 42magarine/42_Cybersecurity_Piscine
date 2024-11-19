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

RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"

def parse_arguments():
    # Create an argument parser with a description
    parser = argparse.ArgumentParser(description="ft_otp")

    # Create a mutually exclusive group
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-g', action='store_true', help='ggg')
    group.add_argument('-k', action='store_true', help='kkk')

    # Add a positional argument for the file
    parser.add_argument('file', help='file')

    args = parser.parse_args()

    # Validate that the file exists
    if not os.path.isfile(args.file):
        print(f"{RED}error: '{args.file}' is not a valid file path or does not exist.{RESET}")
        exit(1)

    # Validate that the file is readable
    if not os.access(args.file, os.R_OK):
        print(f"{RED}error: '{args.file}' is not readable. Check permissions.{RESET}")
        exit(1)

    return args

def generate_key(file_path):
    try:
        with open(file_path, 'r') as file:
            key = file.read()

    except Exception as e:
        print(f"{RED}error: Failed to read file: {e}{RESET}")
        return

    # Strip leading/trailing whitespace, including newlines
    key = key.strip()

    # Check for minimum length
    if len(key) < 64: # oder != 64
        print(f"{RED}error: key must be at least 64 hexadecimal characters.{RESET}")
        return

    # Validate against the pattern
    if not re.fullmatch(r'[0-9a-fA-F]+', key):
        print(f"{RED}error: key must only contains hexadecimal characters.{RESET}")
        return

    print(f"{GREEN}ok{RESET}")

def main():
    args = parse_arguments()

    if args.g:
        generate_key(args.file)
    elif args.k:
        print(f"-k: {args.k}")

    exit(0)

if __name__ == "__main__":
    main()
