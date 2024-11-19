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

RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"

def parse_arguments():
    # Create an argument parser with a description
    parser = argparse.ArgumentParser(description="ft_otp")

    # Create a mutually exclusive group
    group = parser.add_mutually_exclusive_group(required=True)

    # Define the command-line arguments
    group.add_argument('-g', action='store_true', help='ggg')
    group.add_argument('-k', action='store_true', help='kkk')
    parser.add_argument('file', help='file')

    # Parse the command-line arguments
    args = parser.parse_args()

    return args

def main():
    args = parse_arguments()
    if args.g:
        print(f"-g: {args.g}")
    if args.k:
        print(f"-k: {args.k}")

if __name__ == "__main__":
    main()
