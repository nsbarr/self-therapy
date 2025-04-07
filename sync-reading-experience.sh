#!/bin/bash

# Sync the edited reading-experience file to the static directory
echo "Syncing reading-experience files..."
cp reading-experience/index.html static/reading-experience/index.html
echo "Done! The changes will be reflected in your Hugo site."

# Optionally, rebuild the site
if [ "$1" == "--build" ]; then
  echo "Rebuilding Hugo site..."
  hugo
  echo "Site rebuilt successfully."
fi 