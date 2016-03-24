import glob
import os
import traceback

from couchpotato.core.event import addEvent
from couchpotato.core.logger import CPLog
from couchpotato.core.plugins.base import Plugin
from subprocess import check_output, STDOUT, CalledProcessError

log = CPLog(__name__)

EXTENSIONS = ('.avi', '.mkv', '.mpg', '.mp4', '.m4v', '.mov', '.ogm', '.ogv', '.wmv', '.divx', '.asf')
BOOLEAN_ARGS = ['debug', 'force']
TEXT_ARGS = ['config']


class CleanIt(Plugin):

    def __init__(self):
        addEvent('renamer.after', self.callscript)

    def callscript(self, message=None, group=None):
        log.info('Executing CleanIt...')

        renamed_video_files = [f for f in group['renamed_files'] if f.lower().endswith(EXTENSIONS)]
        if not renamed_video_files:
            log.info('No video file.')
            return True

        destination_dir = group['destination_dir']
        subtitles = [f for f in glob.iglob(os.path.join(destination_dir, '*.srt')) if os.path.isfile(f)]
        if not subtitles:
            log.info('No video file.')
            return True

        command = [self.conf('cleanit_cmd')]
        command.extend(self.get_arguments(BOOLEAN_ARGS, boolean=True))
        command.extend(self.get_arguments(TEXT_ARGS))
        command.extend(subtitles)

        try:
            log.info('%s' % command)
            output = check_output(command, stderr=STDOUT)
            log.info('CleanIt was executed successfully')
            log.info(output)
            return True
        except CalledProcessError as cpe:
            log.error(cpe.output)
        except:
            log.error('Failed to call script: %s', (traceback.format_exc()))

        return False

    def get_arguments(self, argument_names, boolean=False):
        results = []
        for argument_name in argument_names:
            if self.conf(argument_name):
                results.append('--' + argument_name.replace('_', '-'))
                if not boolean:
                    results.append(str(self.conf(argument_name)))

        return results
