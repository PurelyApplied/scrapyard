#!/usr/bin/env pythonhttps://www.reddit.com/r/learnpython/comments/5pltzy/is_there_an_easier_way_to_do_this/

"""Initially in responce to the post at
https://www.reddit.com/r/learnpython/comments/5pltzy/is_there_an_easier_way_to_do_this/

This file demonstrates some best practices for user input, error handling, and a simple summation.
"""


# First and foremost, you want to avoid using globals.  It's bad form
# and can lead to some hard-to-diagnose bugs.  As a corollary, you
# want to avoid using any "top-level" variables or function calls that
# aren't going to remain constant throughout the entirety of your module.

# For instance, this is fine

MY_CONSTANT = 10

# but this would not be (and is therefore commented out.

# my_list = []
# index = 0

# ==========

def 
