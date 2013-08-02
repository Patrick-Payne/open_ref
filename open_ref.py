#!/usr/bin/env python3
'''
File: open_ref.py
Author: Patrick Payne
Description: Opens up a specified PDF from the current folder.
'''
import sys
import subprocess

# The program to call in order to open the refs
ref_program = "evince"

def main():
    """Gets the input argument, opens the file. """
    if len(sys.argv) != 2:
        print("Incorrect usage.")
        print("Usage: {0[0]} filename".format(sys.argv))
        sys.exit()

    try:
        # Open the ref with the selected program
        file_name = sys.argv[1]
        file_name = file_name.strip()
        subprocess.Popen([ref_program, file_name], stderr=subprocess.DEVNULL)

    except FileNotFoundError:
        print("{} is not a valid file name.".format(file_name))


if __name__ == '__main__':
    main()
