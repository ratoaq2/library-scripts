# -*- coding: utf-8 -*-
import click
import logging
import os

from cleanit import api
from cleanit.config import Config
from cleanit.subtitle import Subtitle


logger = logging.getLogger('cleanit')


@click.command()
@click.option('-c', '--config', help='YAML config file to be used')
@click.option('-f', '--force', is_flag=True, default=False,
              help='Force saving the subtitle even if there was no change.')
@click.option('--test', is_flag=True, help='Do not make any change. Useful to be used together with --debug')
@click.option('--debug', is_flag=True, help='Print useful information for debugging and for reporting bugs.')
@click.option('-v', '--verbose', count=True, help='Display debug messages')
@click.argument('path', type=click.Path(), required=True, nargs=-1)
def cleanit(config, force, test, debug, verbose, path):
    if debug:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(logging.BASIC_FORMAT))
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)

    cfg = Config.from_file(config)
    if not cfg:
        click.echo('No configuration file is defined. Use --config <config.yml> or create ~/.config/cleanit/config.yml',
                   color='red')
        return

    if not cfg.rules:
        click.echo('No rules defined. Check your configuration file %s' % cfg.path, color='red')
        return

    collected_subtitles = []
    discarded_paths = []

    for p in path:
        scan(p, collected_subtitles, discarded_paths)

    if discarded_paths:
        if len(discarded_paths) == len(path):
            click.echo('Processing input as string...', color='green')
            for value in discarded_paths:
                result = api.clean(value, cfg.rules)
                click.echo(result, color='blue')
            return

        if verbose:
            click.echo('Discarded %s' % discarded_paths, color='red')

    click.echo('Collected %d subtitles' % len(collected_subtitles), color='green')
    for i in reversed(range(len(collected_subtitles))):
        sub = collected_subtitles[i]
        modified = api.clean_subtitle(sub, cfg.rules)
        if (modified or force) and not test:
            click.echo("Saving '%s'" % sub.path, color='green')
            api.save_subtitle(sub)
            click.echo("Saved '%s'" % sub.path, color='green')
        elif verbose > 0:
            click.echo("No modification for '%s'" % sub.path, color='green')
        # to free up memory
        del collected_subtitles[i]


def scan(path, collected, discarded):
    if not os.path.exists(path):
        discarded.append(path)

    elif os.path.isfile(path):
        if path.lower().endswith('.srt'):
            collected.append(Subtitle(path))

    elif os.path.isdir(path):
        for dir_path, dir_names, file_names in os.walk(path):
            for filename in file_names:
                file_path = os.path.join(dir_path, filename)
                scan(file_path, collected, discarded)
