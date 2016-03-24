#!/usr/bin/env python
#
# Post Processing Subtitles Extra Script
#   This script executes cleanit for the given subtitle.
#   https://github.com/ratoaq2/cleanit
#
import os
import sys

lib_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '../lib/'))
if os.path.isdir(lib_folder):
    sys.path.insert(0, lib_folder)

from cleanit.api import clean_subtitle, save_subtitle
from cleanit.config import Config
from cleanit.subtitle import Subtitle


script_path = sys.argv[0]
video_path = sys.argv[1]
subtitle_path = sys.argv[2]
language_code = sys.argv[3]
show_name = sys.argv[4]
season = sys.argv[5]
episode = sys.argv[6]
episode_name = sys.argv[7]
show_indexer_id = sys.argv[8]

config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../cleanit.yml'))

subtitle = Subtitle(subtitle_path)
config = Config.from_file(config_path)
if clean_subtitle(subtitle, config.rules):
    save_subtitle(subtitle)
