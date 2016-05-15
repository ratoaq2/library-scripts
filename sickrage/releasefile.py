#!/usr/bin/env python
#
# Post Processing Extra Script
#   This script will create a .release file alongside the final video file.
#   The release file will contain the original video name (before renaming)
#
import codecs
import os
import sys

EXTENSION = '.release'

script_path = sys.argv[0]
final_video_path = sys.argv[1]
original_video_path = sys.argv[2]
show_indexer_id = sys.argv[3]
season = sys.argv[4]
episode = sys.argv[5]
episode_air_date = sys.argv[6]

original_base_name = os.path.splitext(os.path.basename(original_video_path))[0]
final_dir_name = os.path.dirname(final_video_path)
final_base_name = os.path.splitext(os.path.basename(final_video_path))[0]

with codecs.open(os.path.join(final_dir_name, final_base_name) + EXTENSION, encoding='utf-8', mode='w') as f:
    f.write(original_base_name + '\r\n')
