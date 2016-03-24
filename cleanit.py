#!/usr/bin/env python

import os
import sys
# Ensure lib added to path, before any other imports
lib_folder = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib/'))
if os.path.isdir(lib_folder):
    sys.path.insert(0, lib_folder)

import re
from cleanit.cli import cleanit

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
    sys.exit(cleanit())
