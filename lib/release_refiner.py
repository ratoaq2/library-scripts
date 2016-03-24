# -*- coding: utf-8 -*-
import logging
import os

from guessit import guessit

logger = logging.getLogger('subliminal')


MOVIE_ATTRIBUTES = {'title': 'title', 'year': 'year', 'format': 'format', 'release_group': 'release_group',
                    'resolution': 'screen_size',  'video_codec': 'video_codec', 'audio_codec': 'audio_codec'}
EPISODE_ATTRIBUTES = {'series': 'title', 'season': 'season', 'episode': 'episode', 'title': 'episode_title',
                      'year': 'year', 'format': 'format', 'release_group': 'release_group', 'resolution': 'screen_size',
                      'video_codec': 'video_codec', 'audio_codec': 'audio_codec'}


def refine(video, extension='release', **kwargs):
    """Refine a video by using the original filename present in its info file.

    Several :class:`~subliminal.video.Video` attributes can be found:

      * :attr:`~subliminal.video.Video.title`
      * :attr:`~subliminal.video.Video.series`
      * :attr:`~subliminal.video.Video.season`
      * :attr:`~subliminal.video.Video.episode`
      * :attr:`~subliminal.video.Video.year`
      * :attr:`~subliminal.video.Video.format`
      * :attr:`~subliminal.video.Video.release_group`
      * :attr:`~subliminal.video.Video.resolution`
      * :attr:`~subliminal.video.Video.video_codec`
      * :attr:`~subliminal.video.Video.audio_codec`

    :param video: the video to refine.
    :param bool extension: the info file extension.

    """
    logger.debug('Starting release refiner with extension %s' % extension)
    dirpath, filename = os.path.split(video.name)
    dirpath = dirpath or '.'
    fileroot, fileext = os.path.splitext(filename)
    info_file = os.path.join(dirpath, '%s.%s' % (fileroot, extension))

    # skip if info file doesn't exist
    if not os.path.isfile(info_file):
        logger.debug('Release file %r does not exist' % info_file)
        return

    with open(info_file, 'r') as f:
        release_name = f.read().strip()

    # skip if no release name was found
    if not release_name:
        logger.debug('Release file %r does not contain a release name' % info_file)
        return

    release_path = os.path.join(dirpath, '%s%s' % (release_name, fileext))
    logger.debug('Guessing using %r' % release_path)

    guess = guessit(release_path)
    attributes = MOVIE_ATTRIBUTES if guess.get('type') == 'movie' else EPISODE_ATTRIBUTES
    for key, value in attributes.items():
        old_value = getattr(video, key)
        new_value = guess.get(value)

        if new_value and old_value != new_value:
            setattr(video, key, new_value)
            logger.debug('Attribute %s changed from <%s> to <%s>' % (key, old_value, new_value))
