#`open_ref .py`#

Script I use to quickly pull up reference material (e.g. from a directory of
pdfs). Work in progress. Currently only works in Python 3, but only because I
use subprocess.DEVNULL to suppress stderr output from the programs used to
read the reference documents. This script should be cross platform, but hasn't
been tested outside of a Linux environment.

#Usage#
`open_ref search_term`
This will search for filenames containing `search_term`. If there is a
single search hit, `open_ref` will open it with the program specified in
`config.py`. Otherwise, it will list the matches and allow the user to select
which search hit to open.

You can streamline this process further by creating a concise alias for the
script like I have, and placing them in `.bashrc` or elsewhere. e.g.

    alias oref="path_to_script/open_ref.py"

or

    alias oref="python3 path_to_script/open_ref.py"

# Possible future features: #
 * fuzzy searching.
 * Keep a database of search hits in a dictionary to speed common searches.
