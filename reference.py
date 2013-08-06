#!/usr/bin/env python3
'''
File: reference.py
Author: Patrick Payne
Description: Implementation of the Reference class, used to represent the
    myriad reference documents that appear in my digital library.
'''
from os import path


class Reference(object):
    """
    A class representing a single reference file. Provides the data that
    identify its type, name, and location in the filesystem.
    """
    def __init__(self, root, name):
        """
        Initialize the Reference given the directory it is located in (root)
        and its filename.
        A precondition is that the root and path must be strings:
        >>> Reference(1234, "test.c")
        Traceback (most recent call last):
        ...
        AssertionError: Path root must have str type, instead got <class 'int'>

        >>> Reference("/home/bob", 1234)
        Traceback (most recent call last):
        ...
        AssertionError: File name must have str type, instead got <class 'int'>
        """
        super(Reference, self).__init__()

        assert isinstance(root, str), \
            "Path root must have str type, instead got {0}".format(type(root))
        assert isinstance(name, str), \
            "File name must have str type, instead got {0}".format(type(name))

        # We get the absolute root by converting '~' and environment variables.
        self.root = path.expandvars(path.expanduser(root))
        self.name = name

    def __str__(self):
        """
        The full path of the reference is used as its string representation.
        >>> str(Reference("/test", "test.c"))
        '/test/test.c'
        """
        return self.full_path

    def __repr__(self):
        return 'Reference("{0.root}", "{0.name}")'.format(self)

    @property
    def extension(self):
        """
        Returns the file extension of the Reference if it has a valid one,
        empty string otherwise.
        >>> Reference("/test", "test.c").extension
        '.c'

        >>> Reference("/test", "Makefile").extension
        ''
        """
        return path.splitext(self.name)[1]

    @property
    def full_path(self):
        """
        Returns a string containing the full absolute path of the reference.
        >>> Reference("/test", "test.c").full_path
        '/test/test.c'
        """
        return path.join(self.root, self.name)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
