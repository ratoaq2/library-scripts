from .main import CleanIt


def autoload():
    return CleanIt()

providers = {
}

config = [{
    'name': 'cleanit',
    'groups': [
        {
            'tab': 'renamer',
            'name': 'cleanit',
            'label': 'Clean Subtitles',
            'description': 'after rename',
            'options': [
                {
                    'name': 'enabled',
                    'default': 0,
                    'type': 'enabler',
                },
                {
                    'name': 'cleanit_cmd',
                    'label': 'Cleanit command',
                    'description': 'Full path to cleanit executable',
                    'default': '/usr/local/bin/cleanit',
                    'advanced': True
                },
                {
                    'name': 'config',
                    'description': 'YAML config file to be used',
                    'placeholder': '/home/user/.config/cleanit/config.yml',
                    'advanced': True
                },
                {
                    'name': 'force',
                    'label': 'Force save',
                    'description': 'Force saving the subtitle even if there was no change',
                    'type': 'bool',
                    'default': False,
                    'advanced': True
                },
                {
                    'name': 'debug',
                    'description': 'Print useful information for debugging and for reporting bugs',
                    'type': 'bool',
                    'default': False,
                    'advanced': True
                },
                {
                    'name': 'verbose',
                    'description': 'Increase verbosity',
                    'type': 'int',
                    'placeholder': '2',
                    'advanced': True
                }
            ],
        }
    ],
}]
