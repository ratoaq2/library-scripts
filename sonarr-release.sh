#!/bin/bash
echo "$sonarr_episodefile_scenename" > "${sonarr_episodefile_path%%.*}.release"
