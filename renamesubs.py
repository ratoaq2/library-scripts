#!/usr/bin/env python

import re
import glob
import os
import sys
import fnmatch
from shutil import move


def find_files(directory, pattern):
    for root, dirs, files in os.walk(directory):
        for basename in files:
            if fnmatch.fnmatch(basename, pattern):
                filename = os.path.join(root, basename)
                yield filename


def renamer(dir, files, pattern, replacement):
    for pathname in find_files(dir, files):
        basename = os.path.basename(pathname)
        new_filename = re.sub(pattern, replacement, basename)
        if new_filename != basename:
            target_pathname = os.path.join(os.path.dirname(pathname), new_filename)
            print('Renaming {old} to {new}'.format(old=pathname, new=target_pathname))
            move(pathname, target_pathname)


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print('Usage: {0} <dir> <lang_code> <new_lang_code>'.format(sys.argv[0]))
        exit(1)

    dir = sys.argv[1]
    language_code = sys.argv[2]
    new_language_code = sys.argv[3]
    renamer(dir, '*.{0}.srt'.format(language_code),
            r'^(.*)\.{0}\.srt$'.format(language_code),
            r'\1.{0}.srt'.format(new_language_code))
