from .main import ReleaseFile


def autoload():
    return ReleaseFile()

providers = {
}

config = [{
    'name': 'releasefile',
    'groups': [
        {
            'tab': 'renamer',
            'name': 'releasefile',
            'label': 'Release File',
            'description': 'after rename',
            'options': [
                {
                    'name': 'enabled',
                    'default': 0,
                    'type': 'enabler',
                },
                {
                    'name': 'file_extension',
                    'label': 'File Extension',
                    'default': 'release',
                    'advanced': True
                }
            ],
        }
    ],
}]
