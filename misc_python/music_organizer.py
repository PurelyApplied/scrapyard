#!/usr/bin/env python3

import os
import logging
import sys


def getNamedStreamLogger(name, stream):
    logger = logging.getLogger(name)

    handler = logging.StreamHandler(stream=stream)
    handler.setLevel(logging.DEBUG)

    logger.addHandler(handler)
    return logger


logger = getNamedStreamLogger(__name__, sys.stderr)


class Register:
    def __init__(self):
        self.sha_to_files = {}
        self.big_ass_list_of_full_path_files = []


def get_extensions(start='./'):
    extensions = set()
    raw = set()
    for root, dirs, files in os.walk(start):
        level = root.replace(start, '').count(os.sep)
        indent = ' ' * 4 * (level)
        #print('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            #print('{}{}'.format(subindent, f))
            if '.' in f:
                extensions.add(f.split('.')[-1])
            else:
                print("File {!r} has no extension.".format(f))
                raw.add('{}/{}'.format(root, f))
    return extensions, raw


def identify_bad_folders(start, target_extensions, case_sensitive=False):
    bad = set()
    bad_but_with_sub = set()
    for root, dirs, files in os.walk(start):
        level = root.replace(start, '').count(os.sep)
        indent = ' ' * 4 * (level)
        #print('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        print("Folder: {}".format(root))
        print("Has subdirectories: {}".format(dirs))
        if not any(
                any(ext == f[-len(ext):]
                    or (not case_sensitive and
                        ext.lower() == f[-len(ext):].lower())
                    for f in files)
                for ext in target_extensions):
            print("BAD?")
            print("\n".join("    {}".format(f) for f in files))
            if dirs:
                bad_but_with_sub.add(root)
            else:
                print("Bad!")
                bad.add(root)
    return bad, bad_but_with_sub
