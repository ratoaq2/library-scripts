import glob
import os
import re
import traceback

from couchpotato.core.event import addEvent
from couchpotato.core.logger import CPLog
from couchpotato.core.plugins.base import Plugin
from subprocess import check_output, STDOUT, CalledProcessError

log = CPLog(__name__)

EXTENSIONS = ('.avi', '.mkv', '.mpg', '.mp4', '.m4v', '.mov', '.ogm', '.ogv', '.wmv', '.divx', '.asf')

PASSWORD_PROVIDERS = ['addic7ed', 'legendastv', 'opensubtitles', 'subscenter']
SUBLIMINAL_BOOLEAN_ARGS = ['debug']
SUBLIMINAL_ARGS = ['cache_dir']
DOWNLOAD_MULTI_ARGS = ['language', 'provider']
DOWNLOAD_BOOLEAN_ARGS = ['single', 'force', 'hearing_impaired']
DOWNLOAD_ARGS = ['age', 'encoding', 'min_score', 'max_workers', 'verbose']


class ExternalSubliminal(Plugin):

    def __init__(self):
        addEvent('renamer.after', self.callscript)

    def callscript(self, message=None, group=None):
        log.info('Executing ExternalSubliminal...')

        renamed_video_files = [f for f in group['renamed_files'] if f.lower().endswith(EXTENSIONS)]
        if not renamed_video_files:
            log.info('No video file.')
            return True

        command = [self.conf('subliminal_cmd')]
        for provider in PASSWORD_PROVIDERS:
            if self.conf(provider + '_username') and self.conf(provider + '_username'):
                command.append('--' + provider)
                command.append(self.conf(provider + '_username'))
                command.append(self.conf(provider + '_password'))

        command.extend(self.get_arguments(SUBLIMINAL_BOOLEAN_ARGS, boolean=True))
        command.extend(self.get_arguments(SUBLIMINAL_ARGS))
        command.append('download')

        for argument_name in DOWNLOAD_MULTI_ARGS:
            for argument_value in self.split_value(self.conf(argument_name)):
                command.append('--' + argument_name)
                command.append(argument_value)

        command.extend(self.get_arguments(DOWNLOAD_BOOLEAN_ARGS, boolean=True))
        command.extend(self.get_arguments(DOWNLOAD_ARGS))
        command.extend(renamed_video_files)

        try:
            log.info('%s' % command)
            output = check_output(command, stderr=STDOUT)
            log.info('Subliminal was executed successfully')
            log.info(output)
            destination_dir = group['destination_dir']
            group['subtitles'] = [f for f in glob.iglob(os.path.join(destination_dir, '*.srt')) if os.path.isfile(f)]

            log.info('Subtitles: %s' % group['subtitles'])
            return True
        except CalledProcessError as cpe:
            log.error(cpe.output)
        except:
            log.error('Failed to call script: %s', (traceback.format_exc()))

        return False

    def split_value(self, value):
        return re.split(';\s*|,\s*|\s+', value) if value else []

    def get_arguments(self, argument_names, boolean=False):
        results = []
        for argument_name in argument_names:
            if self.conf(argument_name):
                results.append('--' + argument_name.replace('_', '-'))
                if not boolean:
                    results.append(str(self.conf(argument_name)))

        return results
