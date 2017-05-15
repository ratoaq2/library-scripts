max_workers: 4
providers:
  - legendastv
provider_configs: {legendastv: {username: user, password: pass}}
languages:
  - pt-BR
hearing_impaired: False
only_one: False
directory: /subtitles/
encoding = utf-8
episode_refiners:
  - metadata
  - release
  - tvdb
  - omdb
movie_refiners:
  - metadata
  - release
  - omdb
debug: true
cache_dir: /cache/
