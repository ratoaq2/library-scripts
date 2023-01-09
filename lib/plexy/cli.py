# -*- coding: utf-8 -*-
import typing

import click
import logging

from babelfish import Error as BabelfishError, Language

from plexy import api
from plexy.api import VersionPreference, Context

logger = logging.getLogger('plexy')


class VersionPreferenceParamType(click.ParamType):
    name = 'version_preference'

    def convert(self, value, param, ctx):
        try:
            return VersionPreference[value.upper()]
        except (AttributeError, KeyError):
            self.fail(f"{click.style(f'{value}', bold=True)} is not a version preference")


class LanguageParamType(click.ParamType):
    name = 'language'

    def convert(self, value, param, ctx):
        try:
            return Language.fromietf(value)
        except (BabelfishError, ValueError):
            self.fail(f"{click.style(f'{value}', bold=True)} is not a valid language")


VERSION_PREFERENCE = VersionPreferenceParamType()
LANGUAGE = LanguageParamType()


@click.command()
@click.option('-L', '--library', multiple=True, help='Selected library')
@click.option('-m', '--movie', multiple=True, help='Selected movie')
@click.option('-s', '--series', multiple=True, help='Selected series. Season and episode could also be defined,'
                                                    'e.g. Chernobyl s01e03, The Boys s2')
@click.option('-t', '--token', required=True, help='Plex token')
@click.option('-u', '--user', multiple=True, help='Selected plex user')
@click.option('-p', '--version-preference', required=True, type=VERSION_PREFERENCE,
              help='Version preference')
@click.option('-l', '--language', type=LANGUAGE, help='Language as IETF code, '
                                                      'e.g. en, pt-BR (can be used multiple times).')
@click.option('-a', '--audio-codec', multiple=True, help='Accepted audio codec')
@click.option('-A', '--excluded-audio-codec', multiple=True, help='Excluded audio codec')
@click.option('-c', '--subtitle-codec', multiple=True, help='Accepted subtitle format')
@click.option('-C', '--excluded-subtitle-codec', multiple=True, help='Excluded subtitle format')
@click.option('-g', '--age', help='Filter movies/episodes newer than AGE, e.g. 12h, 1w2d.')
@click.option('--test', is_flag=True, help='Do not make any change. Useful to be used together with --debug')
@click.option('--debug', is_flag=True, help='Print useful information for debugging and for reporting bugs.')
@click.option('-v', '--verbose', count=True, help='Display debug messages')
@click.argument('url', required=True, nargs=1)
def plexit(library: typing.Optional[typing.Tuple[str]],
           movie: typing.Optional[typing.Tuple[str]],
           series: typing.Optional[typing.Tuple[str]],
           token: str,
           user: typing.Optional[typing.Tuple[str]],
           version_preference: VersionPreference,
           language: typing.Optional[Language],
           audio_codec: typing.Optional[typing.Tuple[str]],
           excluded_audio_codec: typing.Optional[typing.Tuple[str]],
           subtitle_codec: typing.Optional[typing.Tuple[str]],
           excluded_subtitle_codec: typing.Optional[typing.Tuple[str]],
           age: typing.Optional[str],
           test: bool,
           debug: bool,
           verbose: int,
           url: str):
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(logging.BASIC_FORMAT))
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG if debug else logging.INFO)

    context = Context(url=url, token=token, libraries=list(library), movies=list(movie), series=list(series),
                      users=list(user), version_preference=version_preference, language=language,
                      audio_codecs=set(audio_codec), excluded_audio_codecs=set(excluded_audio_codec),
                      subtitle_codecs=set(subtitle_codec), excluded_subtitle_codecs=set(excluded_subtitle_codec),
                      age=age, test=test, verbose=verbose)

    api.plexit(context)


if __name__ == '__main__':
    plexit()
