from .main import ExternalSubliminal


def autoload():
    return ExternalSubliminal()

providers = {
}

config = [{
    'name': 'externalsubliminal',
    'groups': [
        {
            'tab': 'renamer',
            'name': 'externalsubliminal',
            'label': 'Download Subtitles (external)',
            'description': 'after rename',
            'options': [
                {
                    'name': 'enabled',
                    'default': 0,
                    'type': 'enabler',
                },
                {
                    'name': 'subliminal_cmd',
                    'label': 'Subliminal command',
                    'description': 'Full path to subliminal executable',
                    'default': '/usr/local/bin/subliminal',
                    'advanced': True
                },
                {
                    'name': 'provider',
                    'description': 'Subliminal Providers',
                    'placeholder': 'addic7ed, legendastv, opensubtitles, podnapisi, subscenter, thesubdb, tvsubtitles',
                },
                {
                    'name': 'addic7ed_username',
                    'label': 'Addic7ed username',
                },
                {
                    'name': 'addic7ed_password',
                    'label': 'Addic7ed password',
                    'type': 'password'
                },
                {
                    'name': 'legendastv_username',
                    'label': 'LegendasTv username',
                },
                {
                    'name': 'legendastv_password',
                    'label': 'LegendasTv password',
                    'type': 'password'
                },
                {
                    'name': 'opensubtitles_username',
                    'label': 'OpenSubtitles username',
                },
                {
                    'name': 'opensubtitles_password',
                    'label': 'OpenSubtitles password',
                    'type': 'password'
                },
                {
                    'name': 'subscenter_username',
                    'label': 'Subscenter username',
                },
                {
                    'name': 'subscenter_password',
                    'label': 'Subscenter password',
                    'type': 'password'
                },
                {
                    'name': 'language',
                    'label': 'Languages',
                    'description': 'Languages as IETF codes (comma-separated)',
                    'placeholder': 'en, pt-BR'
                },
                {
                    'name': 'cache_dir',
                    'label': 'Cache directory',
                    'description': 'Path to the cache directory',
                    'placeholder': '/home/user/.cache/subliminal',
                    'advanced': True
                },
                {
                    'name': 'age',
                    'label': 'Age',
                    'description': 'Filter videos newer than age',
                    'placeholder': '1w2d3h',
                    'advanced': True
                },
                {
                    'name': 'encoding',
                    'label': 'Encoding',
                    'description': 'Subtitle file encoding, default is to preserve original encoding',
                    'advanced': True
                },
                {
                    'name': 'single',
                    'label': 'Single subtitle',
                    'description': 'Save subtitle without language code in the file name, i.e. use .srt extension. '
                                   'Do not use this unless your media player requires it',
                    'type': 'bool',
                    'default': False,
                    'advanced': True
                },
                {
                    'name': 'force',
                    'label': 'Force download',
                    'description': 'Force download even if a subtitle already exist',
                    'type': 'bool',
                    'default': False,
                    'advanced': True
                },
                {
                    'name': 'hearing_impaired',
                    'label': 'Hearing impaired',
                    'description': 'Prefer hearing impaired subtitles',
                    'type': 'bool',
                    'default': False,
                    'advanced': True
                },
                {
                    'name': 'min_score',
                    'label': 'Minimum score',
                    'description': 'Minimum score for a subtitle to be downloaded (0 to 100)',
                    'type': 'int',
                    'default': 90,
                    'advanced': True
                },
                {
                    'name': 'max_workers',
                    'label': 'Maximum workers',
                    'description': 'Maximum number of threads to use',
                    'type': 'int',
                    'default': 1,
                    'advanced': True
                },
                {
                    'name': 'debug',
                    'description': 'Print useful information for debugging subliminal and for reporting bugs',
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
