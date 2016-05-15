# Do not remove all [....] suffixes, or it will break anime releases ## Need to verify this is true now
# Check your database for funky release_names and add them here, to improve failed handling, archiving, and history.
# select release_name from tv_episodes WHERE LENGTH(release_name);
# [eSc], [SSG], [GWC] are valid release groups for non-anime
REMOVE_PATTERNS = {
    r'\[rartv\]$': 'searchre',
    r'\[rarbg\]$': 'searchre',
    r'\.\[eztv\]$': 'searchre',
    r'\[eztv\]$': 'searchre',
    r'\[ettv\]$': 'searchre',
    r'\[cttv\]$': 'searchre',
    r'\.?[[.]vtv\]?$': 'searchre',
    r'\[EtHD\]$': 'searchre',
    r'\[GloDLS\]$': 'searchre',
    r'\[silv4\]$': 'searchre',
    r'\[Seedbox\]$': 'searchre',
    r'\[PublicHD\]$': 'searchre',
    r'\[REQ\]\s$': 'searchre',
    r'\.\[PublicHD\]$': 'searchre',
    r'\.\[NO.RAR\]$': 'searchre',
    r'\[NO.RAR\]$': 'searchre',
    r'-\=\{SPARROW\}\=-$': 'searchre',
    r'\=\{SPARR$': 'searchre',
    r'\.\[\d*(P|p)\]\[HEVC\]$': 'searchre',
    r'\[AndroidTwoU\]$': 'searchre',
    r'\[brassetv\]$': 'searchre',
    r'\[Talamasca32\]$': 'searchre',
    r'\(musicbolt\.com\)$': 'searchre',
    r'\.\(NLsub\)$': 'searchre',
    r'\(NLsub\)$': 'searchre',
    r'\.\[BT\]$': 'searchre',
    r' \[1044\]$': 'searchre',
    r'\.RiPSaLoT$': 'searchre',
    r'\.GiuseppeTnT$': 'searchre',
    r'\.Renc$': 'searchre',
    r'\.gz$': 'searchre',
    r'\.English$': 'searchre',
    r'\.German$': 'searchre',
    r'\.\.Italian$': 'searchre',
    r'\.Italian$': 'searchre',
    r'(?<![57])\.1$': 'searchre',
    r'-NZBGEEK$': 'searchre',
    r'-Siklopentan$': 'searchre',
    r'-Chamele0n$': 'searchre',
    r'-Obfuscated$': 'searchre',
    r'-BUYMORE$': 'searchre',
    r'-\[SpastikusTV\]$': 'searchre',
    r'-RP$': 'searchre',
    r'-20-40$': 'searchre',
    r'\.\[www\.usabit\.com\]$': 'searchre',
    r'^\[www\.Cpasbien\.pe\] ': 'searchre',
    r'^\[www\.Cpasbien\.com\] ': 'searchre',
    r'^\[ www\.Cpasbien\.pw \] ': 'searchre',
    r'^\.www\.Cpasbien\.pw': 'searchre',
    r'^\[www\.newpct1\.com\]': 'searchre',
    r'^\[ www\.Cpasbien\.com \] ': 'searchre',
    r'- \{ www\.SceneTime\.com \}$': 'searchre',
    r'^\{ www\.SceneTime\.com \} - ': 'searchre',
    r'^\]\.\[www\.tensiontorrent.com\] - ': 'searchre',
    r'^\]\.\[ www\.tensiontorrent.com \] - ': 'searchre',
    r'- \[ www\.torrentday\.com \]$': 'searchre',
    r'^\[ www\.TorrentDay\.com \] - ': 'searchre',
    r'\[NO-RAR\] - \[ www\.torrentday\.com \]$': 'searchre',
}


def remove_non_release_groups(name):
    """
    Remove non release groups from name
    """
    if not name:
        return name

    result = name
    for remove_string, remove_type in REMOVE_PATTERNS.iteritems():
        if remove_type == 'search':
            result = result.replace(remove_string, '')
        elif remove_type == 'searchre':
            result = re.sub(r'(?i)' + remove_string, '', result)

    return result
