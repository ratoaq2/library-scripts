# -*- coding: utf-8 -*-
import typing
from collections import defaultdict

from babelfish import Language, LanguageReverseError
from trakit.api import trakit
from plexapi.media import MediaPartStream


def get_title(stream: MediaPartStream):
    return sorted([t for t in {stream.extendedDisplayTitle, stream.displayTitle, stream.title} if t],
                  key=lambda x: len(x),
                  reverse=True)[0]


def get_expected_languages(stream: MediaPartStream):
    languages: typing.Set[Language] = set()
    for code in {stream.languageCode, stream.language, stream.languageTag}:
        if not code:
            continue

        for conv in (Language.fromietf, Language.fromname, Language, Language.fromalpha2):
            try:
                lang = conv(code)
                languages.add(lang)
                break
            except (ValueError, LanguageReverseError):
                pass

    max_num_tags = 0
    more_specific = defaultdict(list)
    for lang in languages:
        num_tags = str(lang).count('-')
        max_num_tags = max(max_num_tags, num_tags)
        more_specific[num_tags].append(lang)

    if more_specific[max_num_tags]:
        return more_specific[max_num_tags]

    return []


def get_language_comparator(target_language: Language):
    def language_cmp(a: MediaPartStream, b: MediaPartStream):
        a_language = a.guessed_language
        b_language = b.guessed_language
        if a_language == b_language:
            for prop in ('commentary', 'closed_caption', 'hearing_impaired'):
                a_prop = a.guess.get(prop)
                b_prop = b.guess.get(prop)
                if not a_prop and b_prop:
                    return -1
                if a_prop and not b_prop:
                    return 1

            return 0
        elif a_language == target_language:
            return -1
        elif b_language == target_language:
            return 1
        elif a_language.alpha3 != b_language.alpha3:
            if a_language.alpha3 == target_language.alpha3:
                return -1
            elif b_language.alpha3 == target_language.alpha3:
                return 1
        else:
            if a_language.country == b_language.country:
                if a_language.script == target_language.script:
                    return -1
                elif b_language.script == target_language.script:
                    return 1
            else:
                if a_language.country == target_language.country:
                    return -1
                elif b_language == target_language.country:
                    return 1

        return (a.index > b.index) - (a.index < b.index)

    return language_cmp


def guess(stream: MediaPartStream):
    title = get_title(stream)
    expected_languages = get_expected_languages(stream)
    options = {'expected_language': expected_languages[0]} if len(expected_languages) == 1 else {}
    guessed = trakit(title, options) if title else {}

    if len(expected_languages) > 1:
        guessed_language = expected_languages[0]
    elif expected_languages:
        guessed_language = expected_languages[0] if 'language' not in guessed else guessed['language']
    else:
        guessed_language = guessed.get('language') or Language('und')

    setattr(stream, 'guess', guessed)
    setattr(stream, 'guessed_language', guessed_language)

    return stream
