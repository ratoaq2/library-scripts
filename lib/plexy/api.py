# -*- coding: utf-8 -*-
import functools
import logging
import typing
from enum import Enum

from babelfish import Language
from plexapi.library import LibrarySection
from plexapi.media import AudioStream, SubtitleStream, Media, MediaPart, VideoStream, MediaPartStream
from plexapi.video import Movie, Episode
from plexapi.server import PlexServer

from plexy.language import guess, get_language_comparator

logger = logging.getLogger(__name__)


class VersionPreference(Enum):
    ORIGINAL = 1
    DUBBED = 2


class Context:

    def __init__(self,
                 url: str,
                 token: str,
                 libraries: typing.List[str],
                 movies: typing.List[str],
                 series: typing.List[str],
                 users: typing.List[str],
                 version_preference: VersionPreference,
                 language: typing.Optional[Language],
                 audio_codecs: typing.Set[str],
                 excluded_audio_codecs: typing.Set[str],
                 subtitle_codecs: typing.Set[str],
                 excluded_subtitle_codecs: typing.Set[str],
                 age: typing.Optional[str],
                 test: bool,
                 verbose: int):
        self.url = url
        self.token = token
        self.libraries = libraries
        self.movies = movies
        self.series = series
        self.users = users
        self.version_preference = version_preference
        self.language = language
        self.audio_codecs = audio_codecs
        self.excluded_audio_codecs = excluded_audio_codecs
        self.subtitle_codecs = subtitle_codecs
        self.excluded_subtitle_codecs = excluded_subtitle_codecs
        self.age = age
        self.test = test
        self.verbose = verbose
        self.all: typing.Set[str] = set()


class Target:

    def __init__(self, title: str, media: MediaPart):
        self.title = title
        self.media = media
        self.video_streams: typing.List[VideoStream] = [guess(stream) for stream in media.videoStreams()]
        self.audio_streams: typing.List[AudioStream] = [guess(stream) for stream in media.audioStreams()]
        self.subtitle_streams: typing.List[SubtitleStream] = [guess(stream) for stream in media.subtitleStreams()]

    @property
    def part(self):
        return self.media

    @property
    def selected_audio(self):
        streams = [stream for stream in self.audio_streams if stream.selected]
        return streams[0] if len(streams) else None

    @property
    def original_language(self):
        languages = [stream.guessed_language for stream in sorted(
            self.video_streams, key=lambda x: x.default or False, reverse=True)
                     if stream.guessed_language]

        if len(languages):
            return languages[0]

        languages = [stream.guessed_language for stream in sorted(
            self.audio_streams, key=lambda x: x.default or False, reverse=True)
                     if stream.guessed_language]

        if len(languages):
            return languages[0]

    @property
    def selected_subtitle(self):
        streams = [stream for stream in self.subtitle_streams if stream.selected]
        return streams[0] if len(streams) else None

    def get_sorted_audio_streams(self, context: Context):
        target_language = context.language if context.version_preference == VersionPreference.DUBBED else self.original_language
        language_cmp = get_language_comparator(target_language)

        return sorted([audio for audio in self.audio_streams if (
                not context.audio_codecs or audio.codec in context.audio_codecs)
                         and audio.codec not in context.excluded_audio_codecs],
                      key=functools.cmp_to_key(language_cmp))

    def get_sorted_subtitle_streams(self, context: Context):
        language_cmp = get_language_comparator(context.language)

        return sorted([subtitle for subtitle in self.subtitle_streams if (
                not context.subtitle_codecs or subtitle.format in context.subtitle_codecs)
                      and subtitle.codec not in context.excluded_subtitle_codecs],
                      key=functools.cmp_to_key(language_cmp))

    def select(self, context: Context):
        audio_streams = self.get_sorted_audio_streams(context)
        selected_audio = audio_streams[0] if len(audio_streams) else self.selected_audio
        if selected_audio != self.selected_audio:
            logger.info('%s - new audio track in %s selected: %s',
                        self.title,
                        selected_audio.guessed_language,
                        selected_audio.displayTitle)
            self.part.setDefaultAudioStream(selected_audio)

        selected_audio_lang = selected_audio.guessed_language if selected_audio else None
        if selected_audio_lang == context.language:
            if self.selected_subtitle:
                logger.info('%s - no subtitle selected', self.title)
                self.part.resetDefaultSubtitleStream()
            return

        subtitle_streams = self.get_sorted_subtitle_streams(context)
        selected_subtitle = subtitle_streams[0] if len(subtitle_streams) else self.selected_subtitle
        if selected_subtitle != self.selected_subtitle:
            logger.info('%s new subtitle in %s selected: %s',
                        self.title,
                        selected_subtitle.guessed_language,
                        selected_subtitle.displayTitle)
            self.part.setDefaultSubtitleStream(selected_subtitle)

    def __repr__(self):
        return f'<{self.__class__.__name__} - {self.title}]>'


def plexit(context: Context):
    plex = PlexServer(context.url, context.token)
    logger.debug('Connected to %s', context.url)

    sections: typing.List[LibrarySection] = plex.library.sections()
    logger.debug('Found %d sections', len(sections))
    filters = {'addedAt>>': context.age} if context.age else None
    for section in sections:
        logger.debug('Entering section %s', section.title)
        episodes: typing.List[Episode] = section.all(libtype='episode')
        logger.debug('Found %d episodes in section %s', len(episodes), section.title)
        for episode in episodes:
            title = f'{episode.grandparentTitle} - {episode.seasonEpisode}'
            logger.debug('Retrieving information for %s', title)
            episode.reload()
            medias: typing.List[Media] = episode.media
            logger.debug('Found %d medias for episode %s', len(medias), title)
            for media in medias:
                parts: typing.List[MediaPart] = media.parts
                for part in parts:
                    logger.debug('Inspecting %s', part.file)
                    target = Target(title, part)
                    target.select(context)

        movies: typing.List[Movie] = section.all(libtype='movie', filters=filters)
        logger.debug('Found %d movies in section %s', len(movies), section.title)
        for movie in movies:
            logger.debug('Retrieving information for movie %s', movie.title)
            movie.reload()
            medias: typing.List[Media] = movie.media
            logger.debug('Found %d medias for movie %s', len(medias), movie.title)
            for media in medias:
                parts: typing.List[MediaPart] = media.parts
                for part in parts:
                    logger.debug('Inspecting %s', part.file)
                    target = Target(movie.title, part)
                    target.select(context)

    for value in context.all:
        print(value)
