import os

from couchpotato.core.event import addEvent
from couchpotato.core.logger import CPLog
from couchpotato.core.plugins.base import Plugin

log = CPLog(__name__)


class ReleaseFile(Plugin):

    def __init__(self):
        addEvent('renamer.after', self.callscript)

    def callscript(self, message=None, group=None):
        log.info('Keep Release Info...')

        original_movie = group['files']['movie'][0]
        original_name = os.path.basename(os.path.splitext(original_movie)[0])
        dirname = group.get('dirname')
        release_path = os.path.join(dirname, original_name) if dirname else original_name
        renamed_filename = group['filename']
        file_extension = self.conf('file_extension')
        release_file = os.path.join(group['destination_dir'], renamed_filename + '.' + file_extension)

        log.info('Creating release file with release name %s ...' % release_path)
        with open(release_file, "w") as text_file:
            text_file.write(release_path + '\r\n')

        return True
