#!/usr/bin/env python
#
# Download subtitle script
#
import logging
import os
import sys
current_folder = os.path.dirname(os.path.realpath(__file__))
lib_folder = os.path.abspath(os.path.join(current_folder, 'lib/'))
if os.path.isdir(lib_folder):
    sys.path.insert(0, lib_folder)

import yaml
from babelfish import Language
from cleanit.api import clean_subtitle, save_subtitle
from cleanit.config import Config
from cleanit.subtitle import Subtitle
from subliminal import (AsyncProviderPool, get_scores, refine, refiner_manager, region, save_subtitles, scan_video,
                        scan_videos)
from subliminal.subtitle import get_subtitle_path

if len(sys.argv) != 2:
    print('Usage: {} videofile.ext'.format(os.path.basename(__file__)))
    exit(-1)

path = sys.argv[1]
debug = True

# Subliminal configuration
with open(os.path.join(current_folder, 'subliminal.yml'), 'r') as f:
    cfg = yaml.safe_load(f)
max_workers = cfg.get('max_workers', 1)
providers = cfg.get('providers')
provider_configs = cfg.get('provider_configs')
languages = {Language.fromietf(l) for l in cfg.get('languages', [])}
hearing_impaired = cfg.get('hearing_impaired', False)
only_one = cfg.get('only_one', False)
directory = cfg.get('directory')
encoding = cfg.get('encoding')
episode_refiners = tuple(cfg.get('episode_refiners'))
movie_refiners = tuple(cfg.get('movie_refiners'))

# cleanit configuration
cleanit_yaml = os.path.join(current_folder, 'cleanit.yml')
config = Config.from_file(cleanit_yaml)

if debug:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(logging.BASIC_FORMAT))
    logging.getLogger('subliminal').addHandler(handler)
    logging.getLogger('subliminal').setLevel(logging.DEBUG)
    logging.getLogger('cleanit').addHandler(handler)
    logging.getLogger('cleanit').setLevel(logging.DEBUG)

region.configure('dogpile.cache.memory')
refiner_manager.register('release = refiners.release:refine')

videos = scan_videos(path) if os.path.isdir(path) else [scan_video(path)]

with AsyncProviderPool(max_workers=max_workers, providers=providers, provider_configs=provider_configs) as p:
    for v in videos:
        refine(v, episode_refiners=episode_refiners, movie_refiners=movie_refiners)
        scores = get_scores(v)
        min_score = scores['hash'] - scores['audio_codec'] - scores['resolution'] - scores['hearing_impaired']
        subtitles = p.download_best_subtitles(p.list_subtitles(v, languages - v.subtitle_languages),
                                              v, languages, min_score=min_score,
                                              hearing_impaired=hearing_impaired, only_one=only_one)
        save_subtitles(v, subtitles, single=only_one, directory=directory, encoding=encoding)
        for s in subtitles:
            subtitle_path = get_subtitle_path(v.name, None if only_one else s.language)
            if directory is not None:
                subtitle_path = os.path.join(directory, os.path.split(subtitle_path)[1])
            subtitle = Subtitle(subtitle_path)
            if clean_subtitle(subtitle, config.rules):
                save_subtitle(subtitle)

