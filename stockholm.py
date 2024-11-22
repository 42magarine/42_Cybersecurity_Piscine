#!/usr/bin/env python3

import argparse

RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"

PROGRAM_VERSION = "1.0.0"

def parse_arguments():
    parser = argparse.ArgumentParser(description="harmless malware")

    parser.add_argument("-v", "--version", action="version", version=f"{YELLOW}%(prog)s {PROGRAM_VERSION}{RESET}", help="Show the program version.")
    parser.add_argument("-r", "--reverse", metavar="KEY", type=str, help="Reverse the infection using the provided key.")
    parser.add_argument("-s", "--silent", action="store_true", help="Run the program without producing any output.")

    args = parser.parse_args()

    return args

def main():
    args = parse_arguments()
    print(f"test")

if __name__ == "__main__":
    main()
