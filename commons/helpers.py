import os
from cleanit.api import clean
from cleanit.config import Config

current_folder = os.path.dirname(os.path.realpath(__file__))
rules_yaml = os.path.join(current_folder, 'release_rules.yml')

RULES = Config.from_file(rules_yaml)


def sanitize_release_name(release_name):
    """Remove non release groups from name

    :param release_name: The release name to be sanitized
    :type release_name: str
    """
    if not release_name:
        return release_name

    return [clean(name, RULES) for name in release_name.split('/')].join('/')
