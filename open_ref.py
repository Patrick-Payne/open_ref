#!/usr/bin/env python3
'''
File: open_ref.py
Author: Patrick Payne
Description: A simple script for quickly searching for and opening reference
   documents. Created to reduce the work needed to pull up a reference text
   to quickly find some command or piece of data, or to consult with books
   like Code Complete or Design Patterns.
'''
import sys
import subprocess
import config
import os
from reference import Reference


class InvalidSearchPath(OSError):
    """
    Raised when the user requests that we search a directory that does not
    exist.
    """
    pass


def main():
    """
    Search a reference folder for reference documents whose
    filenames contain a user-specified search term. Open the document if it
    is the only hit, otherwise print the paths of all the search hits.
    """
    # Get the single search term input by the user.
    if len(sys.argv) == 2:
        search_term = sys.argv[1]
    else:
        print("Incorrect usage.")
        print("Usage: {0[0]} search_term".format(sys.argv))
        sys.exit()

    # Get a list of all the reference documents in the seach paths.
    try:
        references = get_references(config.SEARCH_PATHS,
                                    config.SUPPORTED_UNIX_FILE_EXTENSIONS)
    except InvalidSearchPath as err:
        print("An invalid path was specified in config.py.")
        print(err)
        sys.exit()

    # Filter out the reference documents that do not match the search term.
    matches = find_matching_references(search_term, references)

    # Do nothing if no references contain the search term.
    if len(matches) == 0:
        print("No matches found for search term: {}".format(search_term))
        sys.exit()

    # If we have exactly one search hit, open it.
    elif len(matches) == 1:
        match = matches[0]

    # If we have multiple search hits, show the list to the user so that they
    # can refine their search.
    else:
        for index, match in enumerate(matches):
            print("{0}: {1.full_path}".format(index, match))

        match = matches[get_int("Which reference should be opened?: ", 0)]

    # Launch the match as a background process, suppressing stderr.
    program = config.UNIX_READER_COMMANDS[match.extension]
    subprocess.Popen([program, match.full_path], stderr=subprocess.DEVNULL)


def get_references(search_paths, valid_extensions):
    """
    Returns the list of reference documents (as Reference objects) found in the
    specified list of search paths that contain one of the extensions in
    valid extensions.
    """
    all_files = get_all_files(search_paths)
    return get_valid_files(all_files, valid_extensions)


def find_matching_references(search_term, references):
    """
    Given a list of reference documents (as Reference objects), return a list
    of reference documents that contain matches for the string search_term. A
    reference contains a case-insensitive match for search_term if the string
    search_term appears anywhere in the file name of the reference (not
    including the directory names leading up to the filename).
    >>> find_matching_references("foo", [Reference("/home/bob", "bar.c")])
    []
    >>> find_matching_references("foo", [Reference("/home/bob", "foo.c")])
    [Reference("/home/bob", "foo.c")]
    """
    search_term = search_term.lower()
    return [ref for ref in references if search_term in ref.name.lower()]


def get_valid_files(all_references, valid_extensions):
    """
    Given the list of Reference objects all_references, returns a list of
    Reference objects that actually represent valid files, i.e. those whose
    extension is valid. A Reference has a valid extension if the extension is
    found in the collection valid_extensions.
    >>> get_valid_files([Reference("/foo", "bar.c")], [".pdf", ".doc"])
    []
    >>> get_valid_files([Reference("/foo", "bar.c")], [".c", ".h"])
    [Reference("/foo", "bar.c")]
    """
    return [ref for ref in all_references if ref.extension in valid_extensions]


def get_all_files(search_paths):
    """
    Returns a list of Reference objects representing all of the files found
    recursively in the specified search_paths. Search_paths must be an array of
    strings representing real directories on the system.
    """
    # Expand the instances of "~" and of environment variables in the paths.
    expanded_search_paths = [expand_path(path) for path in search_paths]

    all_files = []
    # Perform the search for files on each of the paths in search_paths.
    for path in expanded_search_paths:
        # Check if the search path actually exists on the file system.
        if not os.path.exists(path):
            raise InvalidSearchPath("{} is an invalid path.".format(path))

        # Get a list of file names in each directory below the search_paths.
        for root, dirs, filenames in os.walk(path):
            # Collect all files found.
            all_files += [Reference(root, filename) for filename in filenames]

    return all_files


def expand_path(raw_path):
    """
    Resolves all instances of the special home character '~' in a path, as well
    as any environment variables (e.g. ${HOME}). Has no effect on paths that
    are already absolute. For example:
    >>> expand_path("/home/bob/reference")
    '/home/bob/reference'
    """
    return os.path.expandvars(os.path.expanduser(raw_path))


def get_int(prompt, default_value=None):
    """
    Gets an integer input from the user, using a given prompt. If the user
    doesn't input anything, just return default_value. If a user inputs an
    invalid input, get_int tells the user that the input is invalid and prompts
    them for new input.
    """
    while True:
        try:
            print(prompt)
            input_string = sys.stdin.read(1)
            if (not input_string) and (default_value is not None):
                return default_value

            input_int = int(input_string)
            return input_int

        except ValueError:
            print("Invalid number entered.")


if __name__ == '__main__':
    main()
