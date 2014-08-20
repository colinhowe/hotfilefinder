hotfilefinder
=============

Finds the 'hottest' files in a git repos history.

Hottest is defined as number of lines changed in a file excluding those lines
changed during creation/deletion of the file.

Output is a list of sorted filenames with their hotness score.

Can be useful for finding files that are likely culprits for being too big or
full of bugs and needing some serious love.

Installation
------------

pip install hotfilefinder

Usage
-----

    > cd somegitrepo
    > hotfilefinder
    README.md 	21
    hotfilefinder/__init__.py 	8
    setup.py 	2


