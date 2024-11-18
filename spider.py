# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    spider.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: maott <maott@student.42.fr>                +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/11/18 11:07:35 by maott             #+#    #+#              #
#    Updated: 2024/11/18 12:15:05 by maott            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import argparse

def main():
    parser = argparse.ArgumentParser(description="The spider program allows you to extract all images from a website recursively by providing a URL as a parameter.")

    parser.add_argument('-r', action='store_true', help='recursively downloads the images in a URL received as a parameter.')
    parser.add_argument('-l', type=int, metavar='[N]', help='indicates the maximum depth level of the recursive download. If not indicated, it will be 5.')
    parser.add_argument('-p', type=str, metavar='[PATH]', help='indicates the path where the downloaded files will be saved. If not specified, ./data/ will be used.')
    parser.add_argument('url', type=str, help='The URL to be processed.')

    args = parser.parse_args()

    if args.l:
        args.r = True
        
    depth = args.l if args.l is not None else 5
    path = args.p if args.p is not None else './data/'

    print(f"-r: {'active' if args.r else 'inactive'}")
    print(f"-l: N= {depth}")
    print(f"-p: PATH= {path}")
    print(f"URL: {args.url}")

if __name__ == "__main__":
    main()
