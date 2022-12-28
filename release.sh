#!/bin/bash
echo "${radarr_moviefile_scenename}${sonarr_episodefile_scenename}" > "${radarr_moviefile_path%.*}${sonarr_episodefile_path%.*}.release"
