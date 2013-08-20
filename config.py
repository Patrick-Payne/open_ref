#!/usr/bin/env python3
'''
File: config.py
Author: Patrick Payne
Description: Some configuration for open_ref.py, detailing where to look
             for PDFs as well as what command to run once they are found.
'''
import os

# For now, only Linux, with evince installed, is supported.
UNIX_READER_COMMANDS = {".pdf": "evince",
                        ".txt": "gvim",
                        ".cpp": "gvim",
                        ".py":  "gvim"}

SUPPORTED_UNIX_FILE_EXTENSIONS = UNIX_READER_COMMANDS.keys()

# The location of the test directory used for doc and unit tests
TEST_DIR = os.path.join(os.getcwd(), "test")

# This is the list of paths that will be searched, NON-RECURSIVELY.
SEARCH_PATHS = ["~/reference", "~/snippets"]

# This is the prefix used to exclude test code.
EXCLUDE_PREFIX = "test_"
