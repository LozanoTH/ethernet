#!/bin/bash

# Auto-update logic
if [ -d ".git" ]; then
    echo "Checking for updates..."
    git fetch origin
    LOCAL=$(git rev-parse HEAD)
    REMOTE=$(git rev-parse @{u})
    if [ "$LOCAL" != "$REMOTE" ]; then
        echo "New version detected! Updating..."
        git pull origin main
        echo "Update complete. Restarting installation..."
        exec bash "$0" "$@"
        exit
    fi
fi

# Dependencies installation
pkg install -y root-repo
pkg install -y git tsu python wpa-supplicant pixiewps iw openssl

echo "Installation/Update finished."

# Launch automatically if requested or just provide info
if [[ "$1" == "--run" ]]; then
    su -c "env PATH=$PATH:/system/bin:/system/bin/xbin python wps.py -i wlan0 -W"
else
    echo "Usage: ./install.sh --run (to install and start the app)"
fi
