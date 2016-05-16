from cleanit.api import clean
from cleanit.config import Config

current_folder = os.path.dirname(os.path.realpath(__file__))
rules_yaml = os.path.join(current_folder, 'release_rules.yml')

RULES = Config.from_file(rules_yaml)


def sanitize_release_name(release_name):
    """
    Remove non release groups from name
    """
    return release_name if not release_name else clean(release_name, RULES)
