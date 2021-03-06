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

from datetime import timedelta
import re
import yaml

from babelfish import Language
from cleanit.api import clean_subtitle, save_subtitle
from cleanit.config import Config
from cleanit.subtitle import Subtitle
from datetime import timedelta
from dogpile.cache.backends.file import AbstractFileLock
from dogpile.util.readwrite_lock import ReadWriteMutex
from subliminal import (
    AsyncProviderPool,
    get_scores,
    refine,
    refiner_manager,
    region,
    save_subtitles,
    scan_video,
    scan_videos
)
from subliminal.cache import region
from subliminal.core import search_external_subtitles
from subliminal.subtitle import get_subtitle_path
from subliminal.video import Movie


class MutexLock(AbstractFileLock):
    """:class:`MutexLock` is a thread-based rw lock based on :class:`dogpile.core.ReadWriteMutex`."""

    def __init__(self, filename):
        """Constructor.
        :param filename:
        """
        self.mutex = ReadWriteMutex()

    def acquire_read_lock(self, wait):
        """Default acquire_read_lock."""
        ret = self.mutex.acquire_read_lock(wait)
        return wait or ret

    def acquire_write_lock(self, wait):
        """Default acquire_write_lock."""
        ret = self.mutex.acquire_write_lock(wait)
        return wait or ret

    def release_read_lock(self):
        """Default release_read_lock."""
        return self.mutex.release_read_lock()

    def release_write_lock(self):
        """Default release_write_lock."""
        return self.mutex.release_write_lock()


def download_subtitle(path):
    # Subliminal configuration
    with open(os.path.join(current_folder, 'subliminal.yml'), 'r') as f:
        cfg = yaml.safe_load(f)
    debug = cfg.get('debug', False)
    cache_dir = cfg.get('cache_dir')

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
    age_match = re.match(r'^(?:(?P<weeks>\d+?)w)?(?:(?P<days>\d+?)d)?(?:(?P<hours>\d+?)h)?$', cfg.get('age', ''))
    age = timedelta(**{k: int(v) for k, v in age_match.groupdict(0).items()}) if age_match else None
    archives = cfg.get('archives', True)
    force = cfg.get('force', False)
    release_group_exceptions = cfg.get('release_group_exceptions', [])

    # cleanit configuration
    cleanit_yaml = os.path.join(current_folder, 'cleanit.yml')
    config = Config.from_file(cleanit_yaml)

    if debug:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(logging.BASIC_FORMAT))
        logger_names = ['cleanit', 'refiners', 'subliminal']
        for logger_name in logger_names:
            l = logging.getLogger(logger_name)
            l.addHandler(handler)
            l.setLevel(logging.DEBUG)

    configure_dogpile_cache(cache_dir)
    refiner_manager.register('release = refiners.release:refine')

    videos = scan_videos(path, age=age, archives=archives) if os.path.isdir(path) else [scan_video(path)]
    with AsyncProviderPool(max_workers=max_workers, providers=providers, provider_configs=provider_configs) as p:
        for v in videos:
            if not force:
                v.subtitle_languages |= set(search_external_subtitles(v.name, directory=directory).values())

            refine(v, episode_refiners=episode_refiners, movie_refiners=movie_refiners, embedded_subtitles=not force)

            scores = get_scores(v)
            min_score = scores['hash'] - scores['audio_codec'] - scores['resolution'] - scores['hearing_impaired'] - 1
            if not v.release_group or v.format in release_group_exceptions:
                min_score -= scores['release_group']

            p.discarded_providers.clear()
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


def configure_dogpile_cache(cache_dir):
    # subliminal cache
    if not cache_dir:
        cache_dir = os.path.join(current_folder, '.cache')

    if not os.path.exists(cache_dir):
        os.mkdir(cache_dir)

    region.configure('dogpile.cache.dbm',
                     expiration_time=timedelta(days=30),
                     arguments={
                         'filename': os.path.join(cache_dir, 'subliminal.dbm'),
                         'lock_factory': MutexLock
                     })


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: {} videofile.ext'.format(os.path.basename(__file__)))
        exit(-1)

    download_subtitle(sys.argv[1])
