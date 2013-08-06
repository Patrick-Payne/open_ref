#!/usr/bin/env python3
'''
File: test.py
Author: Patrick Payne
Description: Runs the doctests for the open_ref tool.
'''
import doctest
import open_ref
import reference

if __name__ == '__main__':
    doctest.testmod(reference, verbose=False)
    doctest.testmod(open_ref, verbose=False)
