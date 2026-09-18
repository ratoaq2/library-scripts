#!/bin/sh

# 1. Define a persistent, writable directory right next to where this script lives
SCRIPT_DIR="$(dirname "$0")"
export HOME="$SCRIPT_DIR/.uv-environment"

# 2. Explicitly point the cache and PATH to this new home
export UV_CACHE_DIR="$HOME/.cache/uv"
export PATH="$HOME/.local/bin:$PATH"

# Ensure the base directory exists
mkdir -p "$HOME"

# 3. Check if uv is installed; if not, download the standalone binary
if ! command -v uv >/dev/null 2>&1; then
    echo "uv not found. Downloading standalone binary..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
fi

# 4. Execute your tool
uvx cleanit "$@"
